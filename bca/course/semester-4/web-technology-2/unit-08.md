---
subject: Web Technology II
grade: BCA Semester 4
unit: 8
title: Content Management Systems and PHP Frameworks
hours: 4
area: BCA 255 · Web Technology II · Unit 8
---

Writing every page from scratch is slow, and most sites need the same things: users, pages, menus, a database, an admin screen. A **content management system (CMS)** gives these ready-made; a **framework** gives structure for building your own. This closing unit covers the CMS part of the old CACS254 outline (Joomla and WordPress at administrator level), and the MVC structure on which both CMSs and frameworks such as Laravel are built.

::: key What this unit gives you
- What a CMS is; WordPress and Joomla concepts at administrator level.
- The MVC pattern with a small working router.
- An orientation to Composer, Laravel and deployment.
:::

**Honesty note.** CMS installation and administration need a web server, a browser and a database, so nothing in this unit except the MVC mini-framework was machine-executed. The steps below describe the standard procedures; menu names differ slightly between versions.

## 8.1 What is a CMS?

A **CMS** separates **content** (text, images) from **design** (themes) and **function** (plugins), stores content in a database (MySQL) and lets non-programmers publish through a web admin panel.

| Feature | WordPress | Joomla |
|---|---|---|
| Main use | blogs, business and news sites; about 40 % of all websites | portals, community and multi-language sites |
| Content unit | **posts** (dated) and **pages** (static) | **articles** in **categories**, plus menus and modules |
| Appearance | **themes** | **templates** |
| Extensions | **plugins** (60,000+) | **extensions**: components, modules, plugins |
| Learning curve | easy | moderate; more built-in structure (ACL, multilingual) |
| Written in | PHP and MySQL | PHP and MySQL, MVC architecture |

### Installing a CMS (the standard steps)

1. Install a LAMP/XAMPP stack and create an empty database and a database user (Unit 3).
2. Download the CMS and unzip it into the web root (`htdocs/mysite`).
3. Open the site in a browser; the installer asks for the database name, user, password, site title and an administrator account (WordPress writes `wp-config.php`; Joomla writes `configuration.php`).
4. Log in to the admin area (`/wp-admin` or `/administrator`).

### WordPress administrator tasks

- **Posts and pages**: create, edit in the block editor, schedule, categorise and tag; set the featured image.
- **Themes**: *Appearance → Themes* to install and activate; *Customize* for logo and colours; child themes keep changes safe from updates.
- **Widgets and menus**: add widgets to sidebars and footers; build navigation menus from pages and categories.
- **Plugins**: add contact forms, SEO, caching, e-commerce (WooCommerce); install only well-maintained plugins, because plugins are the main source of vulnerabilities.
- **Users and roles**: Administrator, Editor, Author, Contributor, Subscriber.
- **Settings**: permalinks (`/%postname%/`), reading and discussion; keep core, themes and plugins updated and take backups.

### Joomla administrator tasks

- **Articles and categories**: create content, assign to categories, feature and publish.
- **Menus and menu items** decide which page appears at each URL; **modules** are boxes placed in template positions (login form, latest news).
- **Extensions manager**: install components (e.g., a forum), modules and plugins; **templates** control layout; template overrides customise output.
- **Users and access levels**: groups with permissions (the ACL system), more granular than WordPress's roles.

**Extending a CMS.** A WordPress plugin is a PHP file with a header comment that registers *hooks* (`add_action`, `add_filter`). A Joomla component follows the MVC structure below. Customisation of the theme/template uses HTML, CSS, JavaScript and PHP.

## 8.2 The MVC pattern

**Model–View–Controller** divides an application into three roles:

| Part | Role | Example |
|---|---|---|
| **Model** | data and business rules; talks to the database | `Student::find(5)`, `$student->average()` |
| **View** | presentation; HTML templates | `students/show.php` |
| **Controller** | receives the request, calls the model, chooses the view | `StudentController::show($id)` |
| **Router** | maps a URL to a controller action | `/students/5` → `show(5)` |

A request flows: browser → router → controller → model (database) → controller → view → response. Separation lets designers and programmers work independently, and each part be tested alone. The program below is a complete miniature of this flow (a router, one controller and a view), runnable without a web server:

```php
<?php
class Student {                                         // Model
    private static array $rows = [1 => ["Ram", 78], 2 => ["Sita", 91]];
    public static function find(int $id): ?array { return self::$rows[$id] ?? null; }
    public static function all(): array { return self::$rows; }
}
function view(string $tpl, array $vars): string {        // View
    $templates = [
        "list" => "<ul>\n{items}</ul>",
        "show" => "<h1>{name}</h1><p>marks: {marks}</p>",
        "404"  => "<h1>Not found</h1>",
    ];
    $out = $templates[$tpl];
    foreach ($vars as $k => $v) { $out = str_replace("{" . $k . "}", $v, $out); }
    return $out;
}
class StudentController {                               // Controller
    public function index(): string {
        $items = "";
        foreach (Student::all() as $id => [$n, $m]) { $items .= "  <li><a href=\"/students/$id\">" . htmlspecialchars($n) . "</a></li>\n"; }
        return view("list", ["items" => $items]);
    }
    public function show(int $id): string {
        $s = Student::find($id);
        return $s ? view("show", ["name" => htmlspecialchars($s[0]), "marks" => (string) $s[1]]) : view("404", []);
    }
}
function route(string $path): string {                  // Router
    if ($path === "/students") return (new StudentController)->index();
    if (preg_match('#^/students/(\d+)$#', $path, $m)) return (new StudentController)->show((int) $m[1]);
    return view("404", []);
}
foreach (["/students", "/students/2", "/students/9", "/nowhere"] as $url) { echo "GET $url\n", route($url), "\n\n"; }
```
```output
GET /students
<ul>
  <li><a href="/students/1">Ram</a></li>
  <li><a href="/students/2">Sita</a></li>
</ul>

GET /students/2
<h1>Sita</h1><p>marks: 91</p>

GET /students/9
<h1>Not found</h1>

GET /nowhere
<h1>Not found</h1>
```
## 8.3 Frameworks and tooling

A **framework** supplies routing, database access (an **ORM**), templating, validation, authentication and security defaults, so you write only the application-specific code.

| Framework | Language | Notes |
|---|---|---|
| **Laravel** | PHP | most popular PHP framework: Eloquent ORM, Blade templates, migrations, Artisan CLI |
| Symfony | PHP | components used by Laravel and Drupal |
| CodeIgniter | PHP | light and simple |
| Django, Flask | Python | the Python equivalents (Python book, Unit 8) |
| Express | JavaScript | Node.js |

**Composer** is PHP's package manager (`composer require vendor/package`; `composer.json` and `composer.lock` record versions; the `vendor/` folder holds packages and an autoloader). A Laravel route and controller look like this (shown, not run here):

```php
// noexec
<?php
// routes/web.php
Route::get('/students/{id}', [StudentController::class, 'show']);

// app/Http/Controllers/StudentController.php
class StudentController extends Controller {
    public function show(int $id) {
        $student = Student::findOrFail($id);          // Eloquent model: SELECT ... WHERE id = ? (prepared)
        return view('students.show', compact('student'));
    }
}
```
### Deploying a PHP site

Choose hosting (shared hosting with cPanel, a VPS, or a cloud platform); upload the code (Git or SFTP); create the production database and a restricted user; set production configuration (`display_errors=Off`, log to a file, secrets in environment variables); enable HTTPS (a free Let's Encrypt certificate); schedule backups; and monitor logs. Keep the document root pointing at the `public/` folder only, so that configuration files are not downloadable.

## Formula and fact sheet

- CMS = content + themes + plugins + admin panel + database. WordPress: posts, pages, themes, plugins. Joomla: articles, categories, menus, modules, extensions, templates.
- MVC: Model (data), View (HTML), Controller (logic), Router (URL → controller).
- Composer manages dependencies; Laravel = routing + Eloquent + Blade + Artisan.
- Deployment: HTTPS, production error settings, restricted DB user, backups, only `public/` exposed.

## Chapter summary

- A CMS lets non-programmers manage content; WordPress and Joomla differ in structure but share themes/templates, plugins/extensions and an admin panel on PHP and MySQL.
- MVC structures applications into model, view, controller and router; frameworks like Laravel provide the plumbing.
- Deployment adds HTTPS, secure configuration and backups.

## Practice

1. List the steps of installing WordPress on a local server.
2. Differentiate a theme and a plugin; a component and a module in Joomla.
3. Explain MVC with the flow of a request.
4. Extend the mini-framework's router with a `/about` route that shows static text.
5. What does Composer do?
6. List five items on a deployment checklist.

::: note Answers and worked solutions
**1.** Install XAMPP; create a database and user; download and unzip WordPress into `htdocs`; open the site and run the installer (database details, site title, admin account); log in at `/wp-admin`.
**2.** A theme controls appearance; a plugin adds functionality. In Joomla a *component* is a full application (main content area, such as articles or a forum); a *module* is a small box in a template position (menu, login box).
**3.** The router matches the URL and calls a controller action; the controller asks the model for data, then passes it to a view; the rendered view is returned as the response (Section 8.2).
**4.**

```php
<?php
function route(string $path): string {
    $routes = ["/about" => "About: BCA Portal, built with PHP."];
    return $routes[$path] ?? "404";
}
echo route("/about"), " | ", route("/x"), "\n";
```
```output
About: BCA Portal, built with PHP. | 404
```
**5.** Composer downloads and updates PHP libraries and their dependencies, records exact versions in `composer.lock`, and generates an autoloader so classes are loaded on demand.
**6.** HTTPS; `display_errors` off and errors logged; restricted database user and secrets outside the code; backups; document root set to `public/`; updated software.
:::
