---
subject: MIS and e-Business
grade: BCA Semester 5
unit: 10
title: Launching a Successful E-Commerce Website
hours: 10
area: BCA 304 · MIS and e-Business · Unit 10
---

An idea becomes an online business only when it is planned, built, hosted, filled with content, made easy to use and found by customers. This unit follows that path: the business plan and cost-benefit case, the process of building a site, domain names, hosting and cPanel, content and catalogue management, design criteria (site map, navigation, grid, colour, usability, performance), payment implementation, and website promotion with search engine optimisation (SEO).

::: key What this unit gives you
- Business plan, cost-benefit analysis, risks, funding and e-commerce model selection.
- The steps of building a website, a hierarchical site structure and build options.
- Domain names, DNS, hosting types and a cPanel walk-through to put a site on a web server.
- Content types, content management and catalogue management.
- Site map, navigation, layout grid, colour, graphics, usability, performance and SEO, with a conversion calculation.
:::

## 10.1 Planning an online business

### The business plan

A **business plan** is a written description of what the business sells, to whom, how it earns money and what it needs to start. For an e-commerce start-up it contains:

1. **Executive summary:** the idea and the goal in half a page.
2. **Market analysis:** target customers, size of demand, competitors and what makes the shop different (its value proposition).
3. **Product and revenue model:** what is sold and how money is made (sales margin, commission, subscription, advertising, delivery fees).
4. **Marketing plan:** how customers will find the site (search, social media, email, partners).
5. **Operations plan:** sourcing or manufacture, stock, packing, delivery, returns and customer support.
6. **Technology plan:** platform, hosting, payment methods and security.
7. **Financial plan:** start-up cost, monthly cost, expected sales, break-even and cash flow.
8. **Risk plan:** what could go wrong and what will be done.

### The cost-benefit case

A **business case** compares costs and benefits to decide whether the project is worth doing. **Costs** are one-time (site development, photography, stock, licences, domain, set-up of payments) and recurring (hosting, staff, marketing, payment fees, delivery, returns). **Benefits** are tangible (sales, saved shop rent, lower order-taking cost) and intangible (brand reach, customer data, goodwill). Use the tools of Unit 9: payback period, NPV and break-even.

::: example A small online clothing shop
One-time cost Rs 3,00,000 (site, photos, first stock, set-up). Monthly fixed cost Rs 40,000 (hosting, staff, tools, ads). Average order Rs 2,500, gross margin 40 percent, so contribution per order is Rs 1,000.
Break-even orders per month = fixed cost ÷ contribution = 40,000 ÷ 1,000 = **40 orders**. If the shop sells 80 orders a month, profit is 80 × 1,000 − 40,000 = Rs 40,000 a month, and the one-time cost is recovered in 3,00,000 ÷ 40,000 = **7.5 months**.
:::

### Risk elements of a business case

- **Market risk:** demand lower than expected or a strong competitor.
- **Technical risk:** site outage, slow performance, failed integration with payment or delivery partners.
- **Financial risk:** funding shortage, high customer-acquisition cost, high return rate.
- **Operational risk:** stock-outs, late delivery, wrong items, poor support.
- **Legal and security risk:** fraud, data leakage, non-compliance with the Electronic Transactions Act and consumer rules.
- **Reputation risk:** a bad review spreading quickly on social media.

For each risk estimate likelihood and impact, plan a response and review it every quarter.

### Funding a new online business

| Source | Description | Suits |
|---|---|---|
| Own savings (bootstrapping) | Founder's money and family support | Small shops, first versions |
| Bank or microfinance loan | Repaid with interest, may need collateral | Businesses with predictable sales |
| Angel investors | Individuals who invest early for a share | Start-ups with a prototype |
| Venture capital | Funds that invest large sums for equity and growth | Scalable platforms |
| Crowdfunding or pre-orders | Customers pay before delivery | Products that need a first batch |
| Grants, incubators, competitions | Support and small funds | Student and social ventures |

### Choosing an e-commerce model

Select the model before building, because it decides features and costs.

| Model | Who sells to whom | Example features |
|---|---|---|
| B2C | Business to consumer | Product catalogue, cart, card or wallet payment |
| B2B | Business to business | Bulk prices, account credit, quotations, purchase orders |
| C2C | Consumer to consumer | Listings, seller ratings, escrow payment |
| Marketplace | Many sellers on one platform | Seller dashboards, commission, dispute handling |
| Subscription | Repeating deliveries or access | Recurring billing, pause and cancel |
| Dropshipping | Shop sells, supplier ships | Supplier feeds, stock sync |
| Service booking | Time slots sold | Calendar, reminders, deposits |

## 10.2 The process of building a website

Building a site follows a repeatable sequence:

1. **Define goals and users.** What should a visitor do (buy, book, enquire)? Who are the visitors?
2. **Choose a domain name and hosting** (section 10.3).
3. **Plan the structure and navigation** (sitemap and wireframes).
4. **Design** the look: layout grid, colours, typography, images.
5. **Develop** the pages and the shop functions: catalogue, search, cart, checkout, account, order tracking.
6. **Create content:** product data, descriptions, policies, help pages.
7. **Integrate** payments, delivery, email and analytics.
8. **Test:** functions, devices and browsers, speed, security, accessibility.
9. **Launch** and then **maintain**: updates, backups, monitoring, new content.

There are four common ways to build:

| Approach | Description | Strengths | Limits |
|---|---|---|---|
| Hand-coded or framework (Django, Laravel, Node.js) | Developers write the shop | Full control, any feature | Highest cost and time |
| Open-source CMS shop (WordPress with WooCommerce, Magento) | Install on your own hosting | Cheap, many plugins, own the data | Needs updates and security care |
| Hosted shop service (Shopify and similar) | Monthly fee, platform runs the servers | Fast launch, secure payments | Fees, less freedom |
| Marketplace storefront (Daraz seller, social shop) | Sell inside another platform | Instant traffic | Commission, no control of the customer relationship |

### Basic hierarchical website structure

A shop is best arranged as a **hierarchy** (a tree): a home page at the top, a few category pages below it, product pages below those, and the cart and checkout reached from any product. A good rule is that any product should be reachable within **three clicks** from the home page. Shallow trees are easy to use; very deep trees hide products from both users and search engines.

```svgfig label="10.1" caption="A hierarchical site structure for an online shop. The home page links to four main sections (Shop, Offers, Help, Account). Shop branches into categories (Men, Women, Kids), and each category branches into product pages. Cart and checkout are reached from any product page. Every product is at most three clicks from the home page."
f = Fig(580, 230)
f.box(240, 8, 100, 32, "Home", fill=BLUE, stroke=NAVY, size=12, bold=True, color=NAVY, r=5)
top = [("Shop", 30), ("Offers", 170), ("Help", 310), ("Account", 450)]
for n, x in top:
    f.box(x, 74, 100, 30, n, fill=MINT, stroke=TEAL, size=11.5, bold=True, color=TEAL, r=5)
    f.arrow([(290, 40), (x + 50, 74)], color=SLATE)
cats = [("Men", 6), ("Women", 76), ("Kids", 146)]
for n, x in cats:
    f.box(x, 140, 62, 28, n, fill=SAND, stroke=AMBER, size=10.5, bold=True, color=AMBER, r=4)
    f.arrow([(80, 104), (x + 31, 140)], color=SLATE)
    f.box(x, 192, 62, 28, "Product", fill=SOFT, stroke=SLATE, size=10, bold=True, color=SLATE, r=4)
    f.arrow([(x + 31, 168), (x + 31, 192)], color=SLATE)
f.box(300, 170, 270, 50, "Cart then Checkout then Payment\nlinked from every product page", fill=ROSE, stroke=RED, size=10.5, bold=True, color=RED, r=5)
```

## 10.3 Website hosting and obtaining a domain name

### Domain names

A **domain name** is the readable address of a site, such as `example.com.np`. It has levels read right to left: the top-level domain (`.np` country code, or `.com`, `.org`), the second-level name chosen by the owner (`example`) and optional sub-domains (`shop.example.com.np`). Steps to obtain one:

1. Check availability with a **registrar** (an accredited seller of names). Names under `.np` are registered through the country-code registry and its authorised registrars; check the current rules because they change.
2. Choose a short, memorable name that is easy to spell, avoids hyphens and numbers, and does not infringe a trademark.
3. Register for a period (usually one to ten years), pay the fee and keep contact details correct, since you must prove ownership.
4. Turn on **auto-renew** and domain privacy; losing a domain by forgetting renewal is a common and costly mistake.

The domain is connected to the server through **DNS records** managed at the registrar or host:

| Record | Meaning | Example |
|---|---|---|
| A | Name to IPv4 address | `example.com.np` to `203.0.113.10` |
| AAAA | Name to IPv6 address | |
| CNAME | Name that is an alias for another name | `www` to `example.com.np` |
| MX | Mail servers for the domain | `mail.example.com.np` priority 10 |
| TXT | Text proof, for example email authentication (SPF, DKIM) | `v=spf1 include:...` |

Changes spread across the Internet within minutes to a day; this delay is the **DNS propagation** time.

### Web hosting

**Hosting** is renting space and computing power on a server connected to the Internet around the clock.

| Type | How it works | Cost and use |
|---|---|---|
| Shared hosting | Many sites share one server | Cheapest; small shops and blogs |
| VPS (virtual private server) | Dedicated slice of a server with its own operating system | Medium; growing shops |
| Dedicated server | One whole machine | High; large sites with special needs |
| Cloud hosting | Resources scale on demand across many machines | Pay as you use; unpredictable traffic |
| Managed e-commerce platform | The vendor runs everything | Monthly fee; no server work |

Choose hosting by uptime guarantee (99.9 percent allows about 8.8 hours of downtime a year), speed and location of the data centre (near customers, or use a CDN), security (backups, SSL, firewall), support and room to grow. Hosting a shop in Nepal gives lower delay for local users; hosting abroad is often cheaper but adds distance and foreign-currency payment.

### cPanel: managing a hosted site

**cPanel** is the web-based control panel offered by many shared and VPS hosts. Its main tools:

| cPanel tool | Used for |
|---|---|
| File Manager | Upload, edit, zip and unzip site files; the public web root is the `public_html` folder |
| FTP Accounts | Create logins for uploading with FTP or SFTP clients such as FileZilla |
| MySQL Databases and phpMyAdmin | Create a database and user, then import or export tables |
| Email Accounts | Create addresses such as `orders@example.com.np` and set forwarding |
| Domains and Zone Editor | Add domains, sub-domains and DNS records |
| SSL/TLS Status | Install a certificate (often free through AutoSSL or Let's Encrypt) |
| Backup | Download full or partial backups and schedule them |
| Cron Jobs | Run scheduled tasks, for example nightly stock sync |
| Metrics (visitors, errors, bandwidth) | Watch traffic and find problems |

**Uploading an e-commerce site to the web server, step by step:**

1. Buy hosting and point the domain's **nameservers** (or A record) to the host; wait for propagation.
2. In cPanel, create a **MySQL database**, a database user with a strong password, and grant the user all privileges on that database.
3. Upload the site files into `public_html` (zip them locally, upload the zip with File Manager and extract), or use SFTP for large sites.
4. Edit the configuration file (for example `wp-config.php` or `.env`) with the database name, user and password. Never leave default credentials.
5. Import the database dump through phpMyAdmin, or run the installer of the CMS.
6. Enable **HTTPS** (install the certificate, then force redirect from `http` to `https`) and set the correct file permissions (files 644, folders 755).
7. Test every function on the live address: browse, search, cart, payment in test mode, order email.
8. Switch payments to live mode, enable scheduled backups and add the site to monitoring and analytics.

## 10.4 Web content creation and management

**Web content** is everything a visitor reads, sees or hears on the site. For a shop it is the product catalogue plus the pages that build trust: about, policies, contact, help and blog.

### Categories and types of content

| Dimension | Types |
|---|---|
| By behaviour | **Static** content (the About page, changes rarely) and **dynamic** content (prices, stock, recommendations generated from a database) |
| By form | Text, images, video, audio, downloads, interactive tools such as size finders |
| By source | Created by the business, supplied by manufacturers, or **user-generated** (reviews, questions, ratings) |
| By purpose | Informational, transactional (cart, checkout), promotional (offers), support (FAQ, returns) |

Good content is accurate, specific, written in the customer's language (Nepali and English where needed), scannable with headings and short paragraphs, and consistent in tone.

### Content management and maintenance

A **content management system (CMS)** lets non-programmers create, edit, approve and publish content, and it keeps content separate from design. Maintenance tasks:

- A **content calendar** for new offers, festival campaigns and blog posts.
- A **workflow** of draft, review, approve and publish, with named responsibilities.
- **Version history** so that an error can be rolled back.
- Regular **audits** to remove out-of-date prices, dead links and discontinued items.
- Keeping **legal pages** (terms, privacy, refund policy) current.

### Catalogue content and its management

The **catalogue** is the structured list of products. Every product record should have:

- A unique **SKU** (stock-keeping unit) and, where available, a barcode.
- A clear **title** (brand, type, key attribute), a **description** with benefits and specifications, and the **price** with currency and tax.
- Several quality **images** with alt text, and sometimes video.
- **Attributes** such as size, colour and material, used for filters and comparison.
- **Category** placement, and **stock** level and delivery time.

Management practices: use a **taxonomy** (category tree) with consistent names; import and export by spreadsheet or product feed for bulk update; synchronise stock with the warehouse so that the site does not sell items that are gone; set rules for pricing and discounts; check data quality (no missing images or duplicate SKUs). Poor catalogue data is the commonest cause of wrong orders, returns and lost search ranking.

## 10.5 Website design criteria

### Site map and navigation

A **site map** has two meanings. The planning **site map** is a diagram of all pages and their links (Figure 10.1). The **XML sitemap** is a file that lists the URLs for search engines:

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com.np/</loc><changefreq>daily</changefreq></url>
  <url><loc>https://example.com.np/shop/men/</loc></url>
</urlset>
```

Good **navigation** gives visitors three answers at once: where am I, where can I go and how do I get back. Use a clear main menu of five to seven items, **breadcrumbs** (Home > Shop > Men > Shirts), a visible search box with suggestions, filters and sort options, consistent footer links and a cart icon that shows the item count.

### Web page layout grid

A **layout grid** divides the page into columns and margins so that elements align. Most responsive sites use a 12-column grid because 12 divides into halves, thirds and quarters. Place the logo, search and cart in the header; the main product area in the middle with filters at the side; and trust information, links and contact in the footer. Put the most important item (the call to action) where the eye lands first, usually top-left or centre, since people scan in an F or Z pattern. On a phone the columns **stack** into one.

```svgfig label="10.2" caption="A shop page on a 12-column grid. The header spans all 12 columns (logo, search, cart). Below it a filter sidebar takes 3 columns and the product area takes 9 columns, holding a row of three product cards of 3 columns each. The footer spans all 12 columns. On a phone the sidebar and cards stack into a single column."
f = Fig(580, 230)
f.box(10, 8, 560, 36, "Header: logo, search, cart (12 columns)", fill=BLUE, stroke=NAVY, size=11, bold=True, color=NAVY, r=4)
f.box(10, 54, 135, 124, "Filters\n(3 columns)", fill=SAND, stroke=AMBER, size=11, bold=True, color=AMBER, r=4)
for i in range(3):
    f.box(155 + i * 140, 54, 130, 100, "", fill=MINT, stroke=TEAL, r=4)
    f.box(165 + i * 140, 62, 110, 52, "image", fill=SOFT, stroke=SLATE, size=10, bold=True, color=SLATE, r=3)
    f.text(220 + i * 140, 132, "Name and price", size=10, color=TEAL, bold=True)
f.text(360, 170, "Product area: 3 cards x 3 columns = 9 columns", size=10.5, color=SLATE, bold=True)
f.box(10, 188, 560, 34, "Footer: policies, contact, payment logos (12 columns)", fill=SOFT, stroke=SLATE, size=11, bold=True, color=SLATE, r=4)
```

### Colour and graphics

Use a limited palette: one main colour, one accent for buttons and one neutral for text. Keep text contrast at least **4.5 to 1** against its background (the WCAG AA rule) so that it is readable in sunlight and by people with weak sight. Do not use colour alone to show meaning (add an icon or text for errors). Compress images (WebP or JPEG), give each an **alt text**, set width and height so the page does not jump, and prefer a few good photographs of the real product over many stock pictures.

### Usability

**Usability** is how easily visitors reach their goals. The widely used heuristics of Jakob Nielsen, applied to a shop:

1. Show the state of the system (order progress, "item added").
2. Use the customer's language, not internal codes.
3. Give control: easy undo, edit cart, cancel.
4. Be consistent across pages.
5. Prevent errors: validate phone numbers and addresses as typed.
6. Make options visible so users recognise instead of remember.
7. Provide shortcuts such as saved addresses and one-click reorder.
8. Keep a minimal design; remove clutter.
9. Help users recover from errors with clear messages.
10. Provide help and contact details on every page.

Reduce checkout friction: allow guest checkout, ask only what is needed, show total cost (delivery and tax) early, support cash on delivery and wallets popular in Nepal, and show security cues.

### Performance

Speed directly affects sales. Google's Core Web Vitals give three targets for a "good" experience: **Largest Contentful Paint (LCP)** within 2.5 seconds, **Interaction to Next Paint (INP)** under 200 milliseconds and **Cumulative Layout Shift (CLS)** below 0.1. Typical improvements: compress and resize images; minify CSS and JavaScript; turn on caching and gzip or Brotli compression; use a CDN; lazy-load images below the fold; avoid heavy plug-ins; keep the server close to users. Measure with Lighthouse or PageSpeed Insights before and after each change.

## 10.6 Implementation of the payment system

A site becomes a shop only when it can take money. The implementation steps are: (1) choose methods that customers use (cards, wallets such as eSewa and Khalti, bank transfer through connectIPS, cash on delivery); (2) open a **merchant account** with a payment service provider; (3) obtain **API keys** and set a test mode; (4) at checkout create an order and redirect or open the provider's payment page, so that card data never touch your server; (5) on return, **verify the payment server-to-server** with the provider's API, not from the browser's redirect alone; (6) mark the order paid, send a confirmation and handle failure and refund cases; (7) test every path (success, failure, timeout, duplicate callback) before going live; (8) store only a token or transaction ID. Unit 7 explains the methods and Unit 8 the security controls.

## 10.7 Website promotion and search engine optimisation (SEO)

A shop nobody finds earns nothing. Promotion has two groups of methods.

**Earned and organic:** SEO, social media posts, email lists, reviews and word of mouth, a useful blog and video content.
**Paid:** search ads (SEM, pay per click), social media ads, marketplace ads, influencer and **affiliate** programmes (commission on sales), and retargeting of people who left without buying.

### SEO

**Search engine optimisation** is improving a site so that it appears higher in unpaid search results. Search engines **crawl** pages, **index** them and **rank** them for a query using hundreds of signals. SEO has three parts:

| Part | Actions |
|---|---|
| **On-page** | Research keywords that buyers type; put the main keyword in the title tag, heading, URL and early text; write unique descriptions for each product; add alt text; use clear headings; link related pages internally |
| **Technical** | HTTPS, mobile-friendly responsive design, fast load, clean URLs, XML sitemap, `robots.txt`, structured data (schema) for products and reviews, no broken links or duplicate pages |
| **Off-page** | Earn **backlinks** from trusted sites, mentions, reviews and social signals; avoid bought links, which risk penalties |

Track results with analytics: visitors, sources, bounce rate, conversion rate, revenue per visitor and keyword positions.

::: example From visitors to orders
Last month the shop had 20,000 visitors. Of them 6 percent added an item to the cart (1,200). Half of those began checkout (600), and 80 percent of those paid (480 orders). With an average order of Rs 2,500, revenue is 480 × 2,500 = **Rs 12,00,000**. The overall conversion rate is 480 ÷ 20,000 = **2.4 percent**. Advertising cost Rs 1,20,000, so the cost per order is 1,20,000 ÷ 480 = **Rs 250**. If a simpler payment step lifts payment success from 80 to 90 percent, orders become 600 × 0.9 = **540**, which is 60 more orders for no extra visitors.
:::

```svgfig label="10.3" caption="The visitor-to-order funnel from the worked example (bar widths not to scale). 20,000 visitors, 1,200 add to cart (6 percent), 600 begin checkout (50 percent of carts), 480 pay (80 percent). Overall conversion is 480 divided by 20,000, which is 2.4 percent. The biggest absolute loss is between visit and cart, but fixing the checkout steps gives the quickest gain."
f = Fig(580, 190)
st = [("Visitors", "20,000", 520, BLUE, NAVY), ("Added to cart", "1,200 (6%)", 380, MINT, TEAL), ("Began checkout", "600 (50%)", 270, SAND, AMBER), ("Paid orders", "480 (80%)", 190, ROSE, RED)]
for i, (a, b, w, fl, c) in enumerate(st):
    y = 8 + i * 44
    f.box(290 - w / 2, y, w, 36, f"{a}: {b}", fill=fl, stroke=c, size=11, bold=True, color=c, r=4)
```

## Chapter summary

- A business plan and cost-benefit case (with break-even, payback and risks) come before any code; choose the funding source and e-commerce model early.
- Building follows goals, domain and hosting, structure, design, development, content, integration, testing, launch and maintenance; shop structure is a shallow hierarchy.
- A domain is connected by DNS records; hosting may be shared, VPS, dedicated, cloud or managed; cPanel provides File Manager, FTP, MySQL, email, SSL and backups for uploading the site.
- Content is static or dynamic, managed by a CMS with workflow; catalogue data need SKUs, attributes, images and stock synchronisation.
- Design criteria: site map and navigation, 12-column grid, accessible colour, usability heuristics and Core Web Vitals performance.
- Payments are integrated through a gateway with server-side verification; promotion combines SEO (on-page, technical, off-page) with paid and social methods and is measured by conversion rate and cost per order.

## Practice

1. List the sections of a business plan for an online shop.
2. A shop has fixed cost Rs 60,000 a month and contribution Rs 1,200 per order. Find the break-even orders.
3. Name four sources of funding for a new online business.
4. Give three differences between B2C, B2B and marketplace models.
5. Write the steps of building an e-commerce website.
6. Explain A, CNAME and MX records.
7. Differentiate shared hosting, VPS and cloud hosting.
8. List the steps to upload a site to a web server using cPanel.
9. Differentiate static and dynamic content with e-shop examples.
10. What fields should a catalogue record contain?
11. What is a 12-column grid and why is it used?
12. State the three Core Web Vitals targets.
13. Explain on-page, technical and off-page SEO.
14. Out of 10,000 visitors, 5 percent add to cart, 40 percent of those begin checkout and 75 percent of those pay. Find the orders and conversion rate.

::: note Answers and worked solutions
**1.** Executive summary, market analysis, product and revenue model, marketing, operations, technology, finance, risks.
**2.** 60,000 ÷ 1,200 = **50 orders** a month.
**3.** Savings, bank loan, angel investors, venture capital, crowdfunding or grants.
**4.** B2C sells to individual consumers with cart and card payment; B2B sells to firms with bulk prices, credit and purchase orders; a marketplace hosts many sellers, takes commission and handles disputes.
**5.** Goals, domain and hosting, structure, design, development, content, integration, testing, launch, maintenance.
**6.** A maps a name to an IPv4 address; CNAME makes one name an alias of another; MX names the mail servers.
**7.** Shared: many sites on one server, cheap. VPS: private slice with its own operating system. Cloud: resources scale on demand across many machines.
**8.** Point DNS, create database and user, upload files to `public_html`, edit configuration, import the database, enable HTTPS, test, go live and schedule backups.
**9.** Static: About page. Dynamic: price and stock pulled from a database.
**10.** SKU, title, description, price, images with alt text, attributes, category, stock and delivery time.
**11.** A layout of 12 equal columns with gutters; 12 splits into halves, thirds and quarters, so layouts align and adapt to screens.
**12.** LCP at most 2.5 s, INP under 200 ms, CLS below 0.1.
**13.** On-page: keywords, titles, content. Technical: HTTPS, speed, mobile, sitemap, structured data. Off-page: backlinks and mentions.
**14.** Carts: 10,000 × 0.05 = 500. Checkouts: 500 × 0.4 = 200. Orders: 200 × 0.75 = **150**. Conversion = 150 ÷ 10,000 = **1.5 percent**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q. Explain the steps to launch an e-commerce website. (10 marks)**

Start with planning: a business plan, a cost-benefit and risk analysis, funding and the choice of model (B2C, B2B, marketplace). Register a domain and buy suitable hosting. Plan a hierarchical structure and navigation, then design the layout on a grid with accessible colours. Develop the shop (catalogue, search, cart, checkout) using a CMS or framework, create content and catalogue data, and integrate a payment gateway with server-side verification, delivery and analytics. Upload to the server by cPanel: create the database, upload files, configure, import data, enable HTTPS. Test functions, devices, speed and security, then launch. After launch, promote through SEO and paid channels, measure conversion and cost per order, back up and update regularly. Close with the usability and performance targets (three clicks, LCP under 2.5 seconds) that decide whether visitors become buyers.

**Q. What is SEO? Describe its types. (5 marks)**

SEO is the practice of improving a site so that search engines rank it higher in unpaid results. On-page SEO improves the content and tags (keyword in title, heading, URL, descriptions, alt text, internal links). Technical SEO makes the site crawlable and fast (HTTPS, mobile-friendly design, sitemap, robots.txt, structured data). Off-page SEO builds authority through backlinks and mentions. Results are measured by traffic, rankings, conversion rate and revenue per visitor.
