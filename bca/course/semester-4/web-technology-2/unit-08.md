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

**Honesty note.** CMS installation and administration need a web server, a browser and a database, so the CMS installation and administration steps were not machine-executed. The PHP programs of this unit (the MVC mini-framework, the router, the hook system, the Composer-style autoloader) and the two-server document-root test of Fig. 8.6 were run for real on PHP 8.2.35. The steps below describe the standard procedures; menu names differ slightly between versions.

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

## 8.4 Seeing the ideas: CMS layers, MVC, hooks, autoloading and deployment

A CMS and a framework both save work by fixing the structure in advance. The plate shows the people and the machines behind these tools, and the figures show how a request is routed, how a plugin changes output through hooks, how Composer finds a class by its name and why the folder you publish matters. Every number comes from a real run on PHP 8.2.35, including two live `php -S` servers.

```photogrid label="8.1" cols="4" ratio="1.0" caption="People and machines behind a site. (a) Matt Mullenweg, co-founder of WordPress, the CMS that powers a large share of the web. (b) Taylor Otwell speaking at Laracon 2013; he created Laravel, the most popular PHP framework. (c) The back of a server rack in a data centre (NASA, public domain): a hosted site is real hardware with power, cooling and cabling, which is why a deployment has to be planned. (d) A cabinet of network switches and patch cables: the traffic of every request passes through equipment like this before it reaches PHP."
@ photo id="bca255/mullenweg" cap="Mullenweg: WordPress"
fit 1.0
focus 0.3 0.4
@ photo id="bca255/otwell" cap="Otwell: Laravel"
fit 1.0
focus 0.62 0.45
@ photo id="bca255/rack" cap="Server rack: hosting"
fit 1.0
focus 0.5 0.5
@ photo id="bca255/switches" cap="Switch cabinet"
fit 1.0
focus 0.5 0.5
```

```svgfig label="8.1" caption="The three layers of a CMS. Content (posts, pages, images) lives in the database, design lives in a theme (WordPress) or template (Joomla), and extra function lives in plugins (WordPress) or extensions (Joomla). The administrator works in the admin panel and never touches PHP; the visitor sees only the finished page. Because the layers are separate, a new theme changes the look without touching the content, and a plugin adds a contact form without touching the theme."
f = Fig(580, 188)
f.box(8, 8, 180, 54, "Admin panel\n(editor, no code)", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(200, 8, 372, 54, "CMS core in PHP: users, roles, menus, routing", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(188, 35), (200, 35)], color=SLATE)
f.box(8, 86, 180, 62, "Content layer\nposts, pages, media\nin MySQL", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(200, 86, 180, 62, "Design layer\ntheme (WordPress)\ntemplate (Joomla)", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(392, 86, 180, 62, "Function layer\nplugins (WordPress)\nextensions (Joomla)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
for x in (98, 290, 482):
    f.arrow([(x, 62), (x, 86)], color=SLATE)
f.text(8, 172, "visitor sees: content + design + function merged into one HTML page", size=10.5, color=NAVY, bold=True, anchor="start")
```

```svgfig label="8.2" caption="One request through the mini MVC framework of Section 8.2, with the real result. The browser asks for /students/2. The router matches the pattern with the number 2 and calls StudentController::show(2). The controller asks the model Student::find(2), which returns Sita with 91 marks. The controller hands the data to the show template, and the real response body was h1 Sita, then a paragraph reading marks: 91. Each part has one job, so the template can be redesigned without touching the data code."
f = Fig(580, 150)
f.box(8, 8, 96, 44, "Browser\nGET /students/2", fill=SOFT, stroke=SLATE, size=10, bold=True)
f.box(124, 8, 96, 44, "Router\nmatches the URL", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(240, 8, 130, 44, "Controller\nshow(2)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(392, 8, 180, 44, "Model\nStudent::find(2)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(104, 30), (124, 30)], color=SLATE)
f.arrow([(220, 30), (240, 30)], color=SLATE)
f.arrow([(370, 20), (392, 20)], color=SLATE)
f.arrow([(392, 42), (370, 42)], color=TEAL)
f.text(482, 66, "returns [Sita, 91]", size=10, color=TEAL, bold=True)
f.box(240, 86, 130, 44, "View\nshow template", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.arrow([(305, 52), (305, 86)], color=SLATE)
f.box(392, 86, 180, 44, "<h1>Sita</h1><p>marks: 91</p>", fill=MINT, stroke=TEAL, size=10, bold=True)
f.arrow([(370, 108), (392, 108)], color=TEAL)
f.text(8, 112, "the response travels back", size=10, color=SLATE, anchor="start")
f.text(8, 126, "to the browser", size=10, color=SLATE, anchor="start")
```

```svgfig label="8.3" caption="What the router does with six real URLs (output of the router, whose pattern accepts only digits as the id). A digit-only id calls show with that number. The URL /students/9 also matches the pattern and reaches the controller, but the model finds no student 9, so the view for 'Not found' is used (real output in Section 8.2). Text such as abc or an extra part like /edit does not match, and an unknown path like /nowhere gets the same 404 view. The pattern is therefore a filter as well as a map: only digits can reach the database query."
f = Fig(580, 232)
f.box(8, 8, 170, 26, "URL requested", fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
f.box(182, 8, 390, 26, "route result (real run)", fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
rows = [("/students", "StudentController::index", 1), ("/students/2", "StudentController::show(2)", 1),
        ("/students/9", "show(9), model finds no row: 404 view", 0), ("/students/abc", "no pattern matches: 404 view", 0),
        ("/students/2/edit", "no pattern matches: 404 view", 0), ("/nowhere", "no pattern matches: 404 view", 0)]
for i, (a, b, ok) in enumerate(rows):
    y = 38 + i * 30
    f.box(8, y, 170, 26, a, fill=SOFT, stroke=SLATE, size=10.5, r=3, anchor="start")
    f.box(182, y, 390, 26, b, fill=MINT if ok else SAND, stroke=TEAL if ok else AMBER, size=10.5, r=3, anchor="start")
f.text(8, 224, "green: handled by a controller   amber: 404 view", size=10, color=SLATE, anchor="start")
```

```svgfig label="8.4" caption="How WordPress-style hooks let a plugin change a page without editing the core, shown with a small hook system run on PHP 8.2.35. A filter receives a value and must return it: the title 'load shedding schedule' passes through the filter of priority 5 (adds the prefix [NEW]) and then priority 10 (upper-case), giving [NEW] LOAD SHEDDING SCHEDULE; the order is decided by the priority number, lowest first. A hook with no filters returns the value unchanged. An action only runs code at a point: the footer action printed 'stats plugin' (priority 10) before 'copyright' (priority 20)."
f = Fig(580, 214)
f.text(8, 14, "Filter hook the_title: a value flows through the functions", size=11, color=NAVY, bold=True, anchor="start")
f.box(8, 26, 126, 48, "load shedding\nschedule", fill=SOFT, stroke=SLATE, size=10)
f.box(160, 26, 126, 48, "priority 5\nadd '[NEW] '", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(312, 26, 126, 48, "priority 10\nupper-case", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(464, 26, 108, 48, "[NEW] LOAD\nSHEDDING SCHEDULE", fill=MINT, stroke=TEAL, size=8.5, bold=True)
for a, b in ((134, 160), (286, 312), (438, 464)):
    f.arrow([(a, 50), (b, 50)], color=SLATE)
f.text(8, 96, "hook with no filters (no_such_hook): value returned unchanged", size=10.5, color=SLATE, anchor="start")
f.line(8, 112, 572, 112, color="#cbd5e1", sw=1)
f.text(8, 130, "Action hook footer: functions run in priority order", size=11, color=NAVY, bold=True, anchor="start")
f.box(8, 142, 270, 40, "priority 10:  footer: stats plugin", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(302, 142, 270, 40, "priority 20:  footer: copyright", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(278, 162), (302, 162)], color=SLATE)
f.text(8, 204, "filter: returns a changed value     action: just runs code at a point", size=10, color=TEAL, bold=True, anchor="start")
```

```svgfig label="8.5" caption="How Composer's autoloader finds a class from its name (real run). The rule of the PSR-4 standard: the namespace prefix App maps to the folder src, and the rest of the class name becomes the file path, so App\Models\Student is loaded from src/Models/Student.php. The first new Student triggered the autoloader once; the second new Student printed no autoload line because the class was already loaded. For App\Models\Nobody no file exists, the loader found nothing and class_exists returned false. No require lines are needed in the program."
f = Fig(580, 212)
f.box(8, 8, 270, 34, "App\\Models\\Student", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.arrow([(143, 42), (143, 70)], color=SLATE, label="prefix App = folder src, slashes for backslashes", lpos=(330, 60), lsize=9.5)
f.box(8, 72, 270, 34, "src/Models/Student.php", fill=MINT, stroke=TEAL, size=12, bold=True)
f.text(8, 130, "real output of the program", size=11, color=NAVY, bold=True, anchor="start")
f.box(8, 140, 564, 24, "autoload: App\\Models\\Student -> src/Models/Student.php     (first new)", fill=SOFT, stroke=SLATE, size=10, anchor="start")
f.box(8, 168, 270, 24, "second new Student: no line (already loaded)", fill=SOFT, stroke=SLATE, size=10, anchor="start")
f.box(286, 168, 286, 24, "Nobody: file missing, class_exists = false", fill=SAND, stroke=AMBER, size=10, anchor="start")
```

```svgfig label="8.6" caption="Why the folder you publish matters, measured with two live PHP servers over the same project. In the left server the document root is the project folder, so everything is reachable: GET /.env returned 200 with the 19 bytes DB_PASSWORD=secret, and /autoload.php (source code) also returned 200. In the right server the document root is the public folder only: /index.php returned 200, while /.env and /autoload.php returned 404 because they lie outside the root. This is why frameworks such as Laravel expose only a public folder."
f = Fig(580, 232)
f.box(8, 8, 276, 28, "document root = project folder", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(296, 8, 276, 28, "document root = public folder", fill=MINT, stroke=TEAL, size=11, bold=True)
L = [("/public/index.php", "200", 1), ("/.env  (19 B: DB_PASSWORD=secret)", "200  LEAK", 0), ("/autoload.php  (source code)", "200  LEAK", 0)]
R = [("/index.php", "200", 1), ("/.env", "404", 1), ("/autoload.php", "404", 1)]
for i in range(3):
    y = 46 + i * 36
    for (x0, row) in ((8, L[i]), (296, R[i])):
        f.box(x0, y, 276, 30, "", fill=SOFT, stroke=SLATE, r=3)
        f.text(x0 + 8, y + 15, row[0], size=9.5, color=SLATE, anchor="start", vmid=True)
        f.text(x0 + 268, y + 15, row[1], size=10.5, color=TEAL if row[2] else RED, bold=True, anchor="end", vmid=True)
f.box(8, 160, 276, 56, "project/\n  .env  autoload.php  src/\n  public/index.php  (all reachable)", fill=ROSE, stroke=RED, size=9.5, anchor="start")
f.box(296, 160, 276, 56, "project/\n  .env  autoload.php  src/   (hidden)\n  public/index.php  (only this is served)", fill=MINT, stroke=TEAL, size=9.5, anchor="start")
```

### 8.4.1 Eight advantages of using a CMS or a framework

1. **Faster delivery.** A CMS gives users, menus, pages and an admin panel on the first day (Fig. 8.1). A college can start a notice and admission site in a weekend instead of months. The team spends time on content and not on login screens.
2. **Content and design are separate.** An editor changes text in the admin panel, and a designer changes the theme without touching the data. A municipality can update its notices daily without asking a programmer. A new theme can change the look of the whole site at once.
3. **Non-programmers can publish.** Roles such as Editor and Author let reporters of a news portal write and schedule articles on their own. The administrator controls who may publish or delete. This frees the developer from routine updates.
4. **Plugins and extensions add features cheaply.** Contact forms, search, SEO, and shop features are installed instead of written. A small business can add online ordering with a ready plugin. Hooks let a plugin change the output without editing the core (Fig. 8.4).
5. **A clear structure keeps big projects tidy.** MVC gives each file one job: the router finds the controller, the controller asks the model and the view shows the result (Fig. 8.2). New team members know where to look. Routes with patterns also keep strange input out of the database (Fig. 8.3).
6. **Security comes built in.** Frameworks such as Laravel use prepared statements in their database layer, escape output in templates and include CSRF tokens. These are the defences of Unit 7, applied by default. A mistake becomes less likely than in hand-written pages.
7. **Composer shares tested code.** One command adds a library, and the autoloader finds every class by its name (Fig. 8.5). The `composer.lock` file makes every developer use the same versions. A team does not have to rewrite a PDF or payment library.
8. **Easier deployment and growth.** Frameworks separate the `public` folder from the private code, so only safe files are served (Fig. 8.6). Configuration lives in environment variables, which differ between a laptop and the server. The same project can move from a lab computer to hosting without code changes.

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

## Model answers (5 and 10 marks)

**Q1. What is a CMS? Compare WordPress and Joomla and explain the steps of installing and administering a CMS. (10 marks)**

**Introduction.** A **content management system (CMS)** is a web application that lets people create, edit and publish content through an admin panel, without writing code. It keeps the content in a database such as MySQL, the design in themes or templates, and the extra features in plugins or extensions (Fig. 8.1). WordPress and Joomla are two popular free CMSs written in PHP and MySQL, and both fit the LAMP/XAMPP stack of Unit 3.

**Comparison.**

| Point | WordPress | Joomla |
|---|---|---|
| Main use | Blogs, business and news sites | Portals, community and multi-language sites |
| Content unit | Posts (dated) and pages (static) | Articles in categories, plus menus and modules |
| Appearance | Themes | Templates |
| Extensions | Plugins (a PHP file with hooks) | Components, modules and plugins |
| Users | Roles: Administrator, Editor, Author, Contributor, Subscriber | Groups with access levels (more detailed ACL) |
| Learning curve | Easy | Moderate, more built-in structure |

**Installation steps.**

1. Install XAMPP or LAMP and create an empty database and a database user.
2. Download the CMS and unzip it into the web root, for example `htdocs/mysite`.
3. Open the site in a browser; the installer asks for the database name, user, password, site title and an administrator account, and writes `wp-config.php` or `configuration.php`.
4. Log in to the admin area (`/wp-admin` or `/administrator`).

**Administration tasks.** The administrator writes posts or articles, creates menus, installs and activates themes or templates, adds plugins or extensions, manages users and roles, and changes settings such as permalinks. Three duties are never optional: keep the core, themes and plugins updated, take regular backups, and install only well-maintained plugins, because plugins are the main source of vulnerabilities (Unit 7).

**Extending a CMS.** A WordPress plugin registers *hooks* with `add_action` and `add_filter` (Fig. 8.4), and a Joomla component follows the MVC structure. Customisation uses HTML, CSS, JavaScript and PHP.

**Conclusion.** A CMS saves time because the user system, admin panel and page structure are ready-made. WordPress suits fast, simple sites, and Joomla suits sites that need more structure and finer access control. Either way, safe updates and backups decide whether the site stays healthy.

**Q2. Explain the MVC pattern with the flow of a request. Write a small router in PHP. (5 marks)**

**MVC (Model–View–Controller)** divides an application into three roles. The **model** holds data and business rules and talks to the database. The **view** is the template that produces HTML. The **controller** receives the request, calls the model and chooses the view. A **router** in front of them maps a URL to a controller action.

**Flow of a request (Fig. 8.2).** The browser sends `GET /students/2`; the router matches the pattern and calls `StudentController::show(2)`; the controller asks `Student::find(2)`; the model returns the data; the controller passes it to the `show` view; the response goes back to the browser. Because each part has one job, designers and programmers can work separately and each part can be tested alone.

A small router with a pattern and a 404 case (real output):

```php
<?php
function route(string $p): string {
    if ($p === "/about") return "About: BCA Portal";
    if (preg_match('#^/students/(\d+)$#', $p, $m)) return "show student " . (int)$m[1];
    return "404 not found";
}
foreach (["/about", "/students/7", "/students/x"] as $u) echo $u, " -> ", route($u), "\n";
```
```output
/about -> About: BCA Portal
/students/7 -> show student 7
/students/x -> 404 not found
```
The pattern accepts only digits, so text such as `x` never reaches the database (Fig. 8.3). The first line shows a fixed route, the second a route with a captured number, and the third falls through to the 404 answer. Real frameworks work the same way, but keep the routes in one file such as `routes/web.php`, so the whole URL map of a site can be read in a minute. In an exam, also state the benefit: because the router, controller, model and view are separate, a change of design does not touch the database code.

**Q3. What is a PHP framework? Explain Laravel's main features, Composer and autoloading. (10 marks)**

**Introduction.** A **framework** is a ready-made structure for building applications. It supplies routing, database access through an **ORM**, templates, validation, authentication and security defaults, so the programmer writes only the code that is special to the application. **Laravel** is the most popular PHP framework (Plate 8.1).

**Main features of Laravel.**

1. **Routing:** `Route::get('/students/{id}', ...)` maps a URL to a controller.
2. **Eloquent ORM:** a model class such as `Student` reads and writes the table with prepared queries, for example `Student::findOrFail($id)`.
3. **Blade templates:** HTML with short directives; output is escaped by default, which prevents XSS.
4. **Migrations:** PHP files that create and change tables, so every developer has the same schema.
5. **Artisan CLI:** commands that create controllers, models and migrations.
6. **Built-in security:** CSRF tokens, password hashing and prepared statements are on by default (Unit 7).

**Composer.** Composer is PHP's package manager. `composer require vendor/package` downloads a library into `vendor/`, `composer.json` lists what the project needs, and `composer.lock` fixes the exact versions so that all developers and the server use the same code. Composer also writes an **autoloader**.

**Autoloading (PSR-4).** The autoloader turns a class name into a file path (Fig. 8.5): the prefix `App` maps to `src`, and namespace separators become folder separators. The program was run for real; it creates the class file in a temporary folder, registers the loader and creates two objects.

```php
<?php
$base = sys_get_temp_dir() . "/psr4_" . getmypid(); mkdir("$base/src/Models", 0777, true);
file_put_contents("$base/src/Models/Student.php", <<<'PHP'
<?php
namespace App\Models;
class Student { public function __construct(public string $name) {} }
PHP);
spl_autoload_register(function (string $class) use ($base) {
    if (strncmp($class, "App\\", 4) !== 0) return;
    $file = $base . "/src/" . str_replace("\\", "/", substr($class, 4)) . ".php";
    echo "autoload: ", $class, " -> ", substr($file, strlen($base) + 1), "\n";
    if (is_file($file)) require $file;
});
$a = new App\Models\Student("Sita"); $b = new App\Models\Student("Ram");
echo $a->name, " and ", $b->name, "\n";
var_dump(class_exists("App\\Models\\Nobody"));
```
```output
autoload: App\Models\Student -> src/Models/Student.php
Sita and Ram
autoload: App\Models\Nobody -> src/Models/Nobody.php
bool(false)
```
**Reading the output.** The loader ran only once, for the first `new Student`, and not for the second, because PHP remembers a class once it is loaded. The class `Nobody` has no file, so the loader found nothing and `class_exists` returned `false`. The program has no `require` line for `Student`: adding a new class needs only a new file in the right folder.

**Conclusion.** A framework such as Laravel gives routing, an ORM, safe templates and migrations, while Composer manages libraries and loads classes by name. Together they reduce repeated code and security mistakes, and they give a team one agreed structure. A student who learns these ideas with plain PHP, as in this unit, can move to Laravel, Symfony or CodeIgniter quickly, because only the names of the functions change.

**Q4. List the main points of deploying a PHP site securely. Why should only the public folder be served? (5 marks)**

**Deployment** is the move of a finished site from the developer's computer to a server that users can reach. A safe deployment has these points: choose hosting (shared hosting with cPanel, a VPS or a cloud platform); upload the code with Git or SFTP; create the production database with a restricted user; set `display_errors=Off` and log errors to a file; keep secrets in environment variables or a `.env` file outside the served folder; serve the site over HTTPS; and set up regular backups and updates.

**Why only the public folder.** The web server publishes every file under its *document root*. If the root is the project folder, configuration and source code become downloadable. The test of Fig. 8.6 used two live servers over one project:

| Request | Root = project folder | Root = public folder |
|---|---|---|
| `/index.php` (the entry file) | 200 | 200 |
| `/.env` (19 bytes, a password) | **200, leaked** | 404 |
| `/autoload.php` (source code) | **200, leaked** | 404 |

With the project folder as root the file `.env` was returned with its content `DB_PASSWORD=secret`. With the `public` folder as root, the same request gave 404 because the file lies outside. For this reason Laravel keeps only `public/index.php` and the assets there, and all other code is outside the document root.

**Q5. What are hooks in WordPress? Differentiate between actions and filters with an example. (5 marks)**

**Hooks** are named points in the WordPress core where a plugin or theme can attach its own function. They let developers change or extend the behaviour of a site without editing the core files, so an update of WordPress does not erase the changes. A plugin registers its function with `add_action` or `add_filter`, and the core calls `do_action` or `apply_filters` at that point. Each registration has a **priority** (default 10): lower numbers run first.

| Point | Action | Filter |
|---|---|---|
| Purpose | Run extra code at a moment | Change a value |
| Return value | Not needed | Must return the (changed) value |
| Core call | `do_action('footer')` | `apply_filters('the_title', $title)` |
| Typical use | Add a script, send a mail, print a footer | Change a title, excerpt or content |

The program is a small copy of the hook system (real output):

```php
<?php
$hooks = [];
function add_filter(string $tag, callable $fn, int $prio = 10): void { global $hooks; $hooks[$tag][$prio][] = $fn; }
function apply_filters(string $tag, $v) { global $hooks; if (empty($hooks[$tag])) return $v; ksort($hooks[$tag]); foreach ($hooks[$tag] as $fns) foreach ($fns as $fn) $v = $fn($v); return $v; }
add_filter("the_title", fn($t) => strtoupper($t));
add_filter("the_title", fn($t) => "[NEW] " . $t, 5);
echo apply_filters("the_title", "load shedding schedule"), "\n";
echo apply_filters("no_such_hook", "unchanged"), "\n";
```
```output
[NEW] LOAD SHEDDING SCHEDULE
unchanged
```
The priority 5 function ran first (the prefix was added) and then the upper-case function (priority 10) changed the whole text, as in Fig. 8.4. A hook with no registered functions returns the value unchanged, so the core keeps working without plugins.
