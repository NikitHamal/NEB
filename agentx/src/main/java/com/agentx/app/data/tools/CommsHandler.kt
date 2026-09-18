package com.agentx.app.data.tools

import android.Manifest
import android.app.Activity
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.Uri
import android.os.Build
import android.provider.ContactsContract
import android.provider.Settings
import android.telephony.SmsManager
import android.telephony.SubscriptionManager
import android.telephony.TelephonyManager
import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.util.FuzzyMatch
import com.agentx.app.util.PermissionUtils
import dagger.hilt.android.qualifiers.ApplicationContext
import java.util.UUID
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.atomic.AtomicInteger
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.withTimeoutOrNull

data class ContactMatch(val name: String, val number: String)

@Singleton
class CommsHandler @Inject constructor(
    @ApplicationContext private val context: Context
) {
    companion object {
        private const val SMS_SENT_ACTION = "com.agentx.app.SMS_SENT"
        private const val SMS_TIMEOUT_MS = 30_000L
    }

    private val smsPending = ConcurrentHashMap<String, CompletableDeferred<Int>>()
    private val smsRequestCode = AtomicInteger(1000)
    @Volatile private var smsReceiverRegistered = false

    private val smsSentReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            val key = intent.getStringExtra("key") ?: return
            smsPending.remove(key)?.complete(resultCode)
        }
    }

    private fun ensureSmsReceiver() {
        if (smsReceiverRegistered) return
        synchronized(this) {
            if (smsReceiverRegistered) return
            val filter = IntentFilter(SMS_SENT_ACTION)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                context.registerReceiver(smsSentReceiver, filter, Context.RECEIVER_NOT_EXPORTED)
            } else {
                @Suppress("DEPRECATION")
                context.registerReceiver(smsSentReceiver, filter)
            }
            smsReceiverRegistered = true
        }
    }

    private fun digitsOf(input: String): String {
        val out = StringBuilder(input.length)
        for (ch in input) {
            if (ch.isDigit() || (ch == '+' && out.isEmpty())) out.append(ch)
        }
        return out.toString()
    }

    private fun looksLikeNumber(input: String): Boolean {
        val digits = digitsOf(input)
        return digits.length >= 7 && digits.length <= 16
    }

    fun searchContacts(name: String, limit: Int = 8): List<ContactMatch> {
        if (!PermissionUtils.has(context, Manifest.permission.READ_CONTACTS)) return emptyList()
        val found = LinkedHashMap<String, ContactMatch>()
        val uri = ContactsContract.CommonDataKinds.Phone.CONTENT_URI
        val projection = arrayOf(
            ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME,
            ContactsContract.CommonDataKinds.Phone.NUMBER
        )
        runCatching {
            context.contentResolver.query(
                uri, projection,
                ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME + " LIKE ?",
                arrayOf("%" + name.replace("%", "").replace("_", "") + "%"),
                ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME + " ASC"
            )?.use { cursor ->
                val nameIdx = cursor.getColumnIndex(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME)
                val numIdx = cursor.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER)
                while (cursor.moveToNext() && found.size < limit * 2) {
                    val cname = cursor.getString(nameIdx).orEmpty().trim()
                    val cnum = cursor.getString(numIdx).orEmpty().trim()
                    if (cname.isEmpty() || cnum.isEmpty()) continue
                    found.putIfAbsent(FuzzyMatch.normalize(cname) + "|" + digitsOf(cnum), ContactMatch(cname, cnum))
                }
            }
        }
        val ranked = FuzzyMatch.rank(name, found.values.toList(), { it.name }, limit)
        return ranked.filter { it.score >= 40 }.map { it.item }
    }

    sealed interface Target {
        data class Number(val number: String) : Target
        data class Single(val contact: ContactMatch) : Target
        data class Choices(val options: List<ContactMatch>) : Target
        data object None : Target
    }

    fun resolveTarget(raw: String): Target {
        val input = raw.trim()
        if (input.isEmpty()) return Target.None
        if (looksLikeNumber(input)) return Target.Number(digitsOf(input))
        if (!PermissionUtils.has(context, Manifest.permission.READ_CONTACTS)) return Target.None
        val matches = searchContacts(input, 5)
        if (matches.isEmpty()) return Target.None
        val top = matches.first()
        val close = matches.filter { it.name.equals(top.name, ignoreCase = true) }
        return if (close.size == 1) Target.Single(top) else Target.Choices(close.take(4))
    }

    fun findContact(spec: ToolCallSpec): ToolExecution {
        val name = spec.arg("name") ?: return ToolExecution.fail("Which name should I look up?")
        if (!PermissionUtils.has(context, Manifest.permission.READ_CONTACTS)) {
            return ToolExecution.needPermission(
                Manifest.permission.READ_CONTACTS, "Contacts",
                "Looking up contacts needs the contacts permission first"
            )
        }
        val matches = searchContacts(name, 5)
        if (matches.isEmpty()) return ToolExecution.fail("No contact matching " + name)
        val lines = StringBuilder()
        matches.forEach { lines.appendLine(it.name + " - " + it.number) }
        return ToolExecution.done(lines.toString().trim())
    }

    fun placeCall(spec: ToolCallSpec): ToolExecution {
        val raw = spec.arg("target") ?: return ToolExecution.fail("Who should I call?")
        return when (val target = resolveTarget(raw)) {
            is Target.Number -> dial(target.number, target.number)
            is Target.Single -> dial(target.contact.number, target.contact.name)
            is Target.Choices -> ToolExecution.fail(
                "Which one? " + target.options.joinToString(", ") { it.name + " (" + it.number + ")" },
                options = target.options.map { "Call " + it.name }
            )
            is Target.None -> {
                if (!PermissionUtils.has(context, Manifest.permission.READ_CONTACTS)) {
                    ToolExecution.needPermission(
                        Manifest.permission.READ_CONTACTS, "Contacts",
                        "Calling a name needs the contacts permission first"
                    )
                } else {
                    ToolExecution.fail("No contact or number matching " + raw)
                }
            }
        }
    }

    private fun dial(number: String, label: String): ToolExecution {
        return if (PermissionUtils.has(context, Manifest.permission.CALL_PHONE)) {
            val intent = Intent(Intent.ACTION_CALL, Uri.parse("tel:" + Uri.encode(number))).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            runCatching { context.startActivity(intent) }.onFailure {
                return ToolExecution.fail("Could not place the call")
            }
            ToolExecution.done("Calling " + label)
        } else {
            val intent = Intent(Intent.ACTION_DIAL, Uri.parse("tel:" + Uri.encode(number))).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            runCatching { context.startActivity(intent) }.onFailure {
                return ToolExecution.fail("Could not open the dialer")
            }
            ToolExecution.done("Dialer opened for " + label + " - tap call to connect")
        }
    }

    suspend fun sendMessage(spec: ToolCallSpec): ToolExecution {
        val raw = spec.arg("target") ?: return ToolExecution.fail("Who should I text?")
        val text = spec.arg("text") ?: return ToolExecution.fail("What should the message say?")
        if (text.length > 1000) return ToolExecution.fail("That message is too long (1000 characters max)")
        return when (val target = resolveTarget(raw)) {
            is Target.Number -> sendSms(target.number, target.number, text)
            is Target.Single -> sendSms(target.contact.number, target.contact.name, text)
            is Target.Choices -> ToolExecution.fail(
                "Which one? " + target.options.joinToString(", ") { it.name + " (" + it.number + ")" },
                options = target.options.map { "Text " + it.name }
            )
            is Target.None -> {
                if (!PermissionUtils.has(context, Manifest.permission.READ_CONTACTS)) {
                    ToolExecution.needPermission(
                        Manifest.permission.READ_CONTACTS, "Contacts",
                        "Texting a name needs the contacts permission first"
                    )
                } else {
                    ToolExecution.fail("No contact or number matching " + raw)
                }
            }
        }
    }

    private suspend fun sendSms(number: String, label: String, text: String): ToolExecution {
        if (!PermissionUtils.has(context, Manifest.permission.SEND_SMS)) {
            val intent = Intent(Intent.ACTION_SENDTO, Uri.parse("smsto:" + Uri.encode(number))).apply {
                putExtra("sms_body", text)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            runCatching { context.startActivity(intent) }.onFailure {
                return ToolExecution.fail("Could not open messaging")
            }
            return ToolExecution.done("Message ready for " + label + " - tap send to deliver")
        }
        return sendSmsDirect(number, label, text)
    }

    private suspend fun sendSmsDirect(number: String, label: String, text: String): ToolExecution {
        if (isAirplaneModeOn()) {
            return ToolExecution.fail("Airplane mode is on. Turn it off to send SMS.")
        }
        val telephony = context.getSystemService(Context.TELEPHONY_SERVICE) as TelephonyManager
        if (telephony.simState != TelephonyManager.SIM_STATE_READY) {
            return ToolExecution.fail("No ready SIM found. SMS needs an active SIM card.")
        }
        val subId = SmsManager.getDefaultSmsSubscriptionId()
        if (subId == SubscriptionManager.INVALID_SUBSCRIPTION_ID) {
            return ToolExecution.fail("No default SIM for SMS. Choose one in SIM settings first.")
        }
        val sms = SmsManager.getSmsManagerForSubscriptionId(subId)
        ensureSmsReceiver()
        val parts = if (text.length > 160) sms.divideMessage(text) else listOf(text)
        val keys = parts.map { UUID.randomUUID().toString() }
        val deferreds = keys.map { key ->
            CompletableDeferred<Int>().also { smsPending[key] = it }
        }
        val intents = keys.map { key ->
            PendingIntent.getBroadcast(
                context,
                smsRequestCode.getAndIncrement(),
                Intent(SMS_SENT_ACTION).putExtra("key", key).setPackage(context.packageName),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
        }
        try {
            if (parts.size == 1) {
                sms.sendTextMessage(number, null, parts[0], intents[0], null)
            } else {
                sms.sendMultipartTextMessage(number, null, parts, ArrayList(intents), null)
            }
        } catch (e: Exception) {
            keys.forEach { smsPending.remove(it) }
            intents.forEach { runCatching { it.cancel() } }
            return ToolExecution.fail("Could not hand the message to the radio: " + (e.message ?: "send failed"))
        }
        val codes = withTimeoutOrNull(SMS_TIMEOUT_MS) {
            deferreds.map { it.await() }
        }
        keys.forEach { smsPending.remove(it) }
        if (codes == null) {
            return ToolExecution.fail("Timed out waiting for the cellular radio. The message may still go out - check with the recipient.")
        }
        for (index in codes.indices) {
            val reason = smsErrorReason(codes[index])
            if (reason != null) {
                return ToolExecution.fail("Part " + (index + 1) + " of " + codes.size + " failed: " + reason)
            }
        }
        val suffix = if (parts.size > 1) " in " + parts.size + " parts" else ""
        return ToolExecution.done("Message sent to " + label + suffix + " (confirmed by radio)")
    }

    private fun smsErrorReason(code: Int): String? = when (code) {
        Activity.RESULT_OK -> null
        SmsManager.RESULT_ERROR_NO_SERVICE -> "no cellular service"
        SmsManager.RESULT_ERROR_RADIO_OFF -> "radio is off (airplane mode?)"
        SmsManager.RESULT_ERROR_NULL_PDU -> "message encoding failed"
        SmsManager.RESULT_ERROR_GENERIC_FAILURE -> "carrier rejected it (check SIM balance and plan)"
        else -> "radio error " + code
    }

    private fun isAirplaneModeOn(): Boolean {
        return runCatching {
            Settings.Global.getInt(context.contentResolver, Settings.Global.AIRPLANE_MODE_ON, 0) != 0
        }.getOrDefault(false)
    }
}
