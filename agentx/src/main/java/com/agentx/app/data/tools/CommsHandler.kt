package com.agentx.app.data.tools

import android.Manifest
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.ContactsContract
import android.telephony.SmsManager
import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.util.FuzzyMatch
import com.agentx.app.util.PermissionUtils
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

data class ContactMatch(val name: String, val number: String)

@Singleton
class CommsHandler @Inject constructor(
    @ApplicationContext private val context: Context
) {
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

    fun sendMessage(spec: ToolCallSpec): ToolExecution {
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

    private fun sendSms(number: String, label: String, text: String): ToolExecution {
        if (PermissionUtils.has(context, Manifest.permission.SEND_SMS)) {
            return try {
                val sms = context.getSystemService(Context.TELEPHONY_SERVICE)?.let {
                    SmsManager.getDefault()
                } ?: SmsManager.getDefault()
                if (text.length > 160) {
                    val parts = sms.divideMessage(text)
                    sms.sendMultipartTextMessage(number, null, parts, null, null)
                } else {
                    sms.sendTextMessage(number, null, text, null, null)
                }
                ToolExecution.done("Message sent to " + label)
            } catch (e: Exception) {
                ToolExecution.fail("Could not send: " + (e.message ?: "radio busy"))
            }
        }
        val intent = Intent(Intent.ACTION_SENDTO, Uri.parse("smsto:" + Uri.encode(number))).apply {
            putExtra("sms_body", text)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        runCatching { context.startActivity(intent) }.onFailure {
            return ToolExecution.fail("Could not open messaging")
        }
        return ToolExecution.done("Message ready for " + label + " - tap send to deliver")
    }
}
