---
file: NEBians-IOE-Past-Paper-Foundation-of-Data-Science-ENCT202-2081-Chaitra.pdf
subject: Foundation of Data Science
level: BE · Year II / Part I
code: ENCT202
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
How is a programmer different from a data scientist? Explain the differences in terms of skill requirements and the various roles available for data scientists in the job market. [[5]]

@q 2
a) Why is K-fold cross validation considered as the standard method for validating model? Explain all the terms; training data, testing data, validating data and fold and overall steps. [[3]]

b) Considering the test data size as 50,000, a typical classification model experimentation results are as shown on the confusion matrix.

| ACTUAL CLASS | Predicted: Yes | Predicted: No |
|---|---|---|
| Yes | 1000 | 1000 |
| No | 1000 | 47000 |

i) Calculate Accuracy, Precision and $F_1$-score measure data as per table below. [[3]]

ii) Explain the difference on resulted accuracy and $F_1$-score value that you have calculated. [[2]]

@q 3
a) Prepare a note on Central Limit Theorem. Why this is considered as important in data analysis and other tasks? Briefly explain. [[4]]

b) An e-mail filter is planned to separate valid e-mails from spam. The word free occurs in 70% of the spam messages and only 4% of the valid messages. Also, 25% of the messages are spam. Determine the following probabilities: [[6]]

(i) The message contains free. (ii) The message is spam given that it contains free. (iii) The message is valid given that it does not contain free.

@q 4
a) What is semi-structured data? How it is different than structured and unstructured data? Explain briefly. [[3]]

b) How do you handle missing data during data preprocessing? Briefly explain two methods illustrating with a small sample data example. [[4]]

@q 5
Here is the 10 random sample data of graduate student age from Sociology and Political Science program class.

| Data# | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Age (Women) | 35 | 29 | 32 | 23 | 36 |
| Age (Men) | 28 | 25 | 29 | 24 | 23 |

(Show your all calculations and consider all 10 data as a single sample.)

a) Calculate normalized ages of 2-students (Data #1, both Women and Men) using z-score and min-max of Zero-to-one. [[4]]

b) Using the same data above, draw a box-plot for depiction of all 10 student age distribution. You need to show all calculations and label the plot properly. [[4]]

@q 6
a) What are the purposes of data visualization? Explain with an example of heat-map based visualization. [[5]]

b) What is regression, and how does it support predictive analytics? Explain with a small sample business application. [[5]]

@q 7
Write brief notes on: (Any Three) [[3×4]]

(i) GDPR (ii) Feature selection (iii) Generative AI (iv) Performance measure using MAE
<!-- SOLUTIONS -->

@s 1
A **programmer** builds software that follows explicit rules written by a human; a **data scientist** extracts knowledge and predictions from data, often with models that *learn* the rules from examples. Both write code, but the goal, the tools and the way success is judged differ.

| Aspect | Programmer (software developer) | Data scientist |
|---|---|---|
| Main goal | Build reliable, efficient software or a system that meets a specification | Answer a question or predict an outcome from data and turn it into a decision or a product |
| Input | Requirements, algorithms, APIs | Raw, messy, often incomplete data and a business problem |
| Typical output | Application, service, library | Insight, report, dashboard, trained and deployed model |
| Logic | Deterministic: the programmer writes the rules | Probabilistic: the rules are learned from data and carry uncertainty |
| Core skills | Data structures and algorithms, OOP, databases, testing, version control, system design | Statistics and probability, linear algebra, machine learning, data wrangling, visualization, domain knowledge, communication |
| Tools | Java, C++, Python, JavaScript, Git, IDEs, CI/CD | Python / R, pandas, NumPy, scikit-learn, TensorFlow / PyTorch, SQL, Jupyter, Tableau / Power BI, Spark |
| Success measure | Correctness, speed, maintainability, zero bugs | Accuracy, precision / recall, business impact, statistical validity |
| Process | Design, code, test, deploy | Ask, collect, clean, explore, model, validate, communicate, monitor |

**Skills a data scientist needs:** (1) mathematics and statistics (distributions, hypothesis testing, regression); (2) programming (Python / R, SQL); (3) data wrangling and databases; (4) machine learning and model evaluation; (5) data visualization and storytelling; (6) domain knowledge and curiosity; (7) soft skills: communication with non-technical people and teamwork.

**Roles in the job market**

- **Data analyst:** SQL, spreadsheets, dashboards, descriptive statistics, reports for business teams.
- **Data scientist:** exploratory analysis, statistical modelling, predictive models, experiments (A/B tests).
- **Machine learning engineer:** puts models into production: pipelines, APIs, scaling, monitoring.
- **Data engineer:** builds and maintains the data pipelines, warehouses and lakes (ETL, Spark, Kafka).
- **Business intelligence (BI) developer:** designs reports and dashboards for decision makers.
- **Research / AI scientist:** develops new algorithms (deep learning, NLP, computer vision).
- **Data / analytics manager and data architect:** lead teams, set data strategy, governance and design the data platform.

In short: a programmer is judged by *whether the program works as specified*, a data scientist by *whether the conclusions from the data are correct and useful*.

@s 2
**(a) K-fold cross validation.**

*Terms.*

- **Training data:** the part of the data on which the model parameters are learned (fitted).
- **Validation data:** a part held back during development, used to tune hyper-parameters and to choose between models; the model never learns from it directly.
- **Testing data:** a final, untouched part used only once to report the unbiased performance of the chosen model on unseen data.
- **Fold:** one of the $K$ equal-sized, non-overlapping subsets into which the data set is split.

*Overall steps.*

1. Shuffle the data set and split it into $K$ folds of (almost) equal size (commonly $K=5$ or $10$; use stratified folds for classification so each fold keeps the class ratio).
2. For $i=1,\dots,K$: keep fold $i$ as the validation (test) fold, train the model on the other $K-1$ folds, and compute the score $s_i$ (accuracy, $F_1$, ...) on fold $i$.
3. Every fold is used exactly once for validation and $K-1$ times for training.
4. The final performance is the mean $\bar s=\frac1K\sum s_i$ (with the standard deviation as a measure of stability). Finally, the model is re-trained on all the training data and evaluated once on the hold-out test set.

```figure caption="5-fold cross validation: each round holds out a different fold for validation (red) and trains on the other four (blue); the final score is the mean of the five scores. A separate test set is kept aside."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(7.2,3.0)); ax.axis("off"); ax.set_xlim(0,10.6); ax.set_ylim(0,6.4)
for r in range(5):
    y=5.2-r*0.95
    ax.text(0.0,y+0.05,"Round %d"%(r+1),fontsize=8,va="center")
    for f in range(5):
        v=(f==r)
        ax.add_patch(mp.Rectangle((1.3+f*1.4,y-0.3),1.4,0.6,fc="#f4b6b6" if v else "#cfe3ff",ec=INK,lw=1.0))
        ax.text(1.3+f*1.4+0.7,y,"Fold %d"%(f+1)+("\nvalidate" if v else ""),ha="center",va="center",fontsize=6.3)
    ax.text(8.55,y,"score $s_%d$"%(r+1),fontsize=8,va="center")
ax.add_patch(mp.Rectangle((9.5,0.8),1.0,4.8,fc="#dff2df",ec=INK,lw=1.0)); ax.text(10.0,3.2,"Test\nset\n(final,\nused once)",ha="center",va="center",fontsize=7)
ax.text(4.3,0.45,"mean score $=\\frac{1}{5}\\sum s_i$",fontsize=9,ha="center",color=ACCENT)
```

*Why it is the standard.* A single train/test split depends on the luck of the split; K-fold uses **all** data for both training and validation, gives $K$ estimates (so the mean and the variance of performance), reduces over-fitting to one split, works well with small data sets and helps in choosing hyper-parameters.

**(b)(i) Metrics.** Total test size $=1000+1000+1000+47000=50\,000$. From the table: $TP=1000$, $FN=1000$, $FP=1000$, $TN=47000$.

$$\text{Accuracy}=\frac{TP+TN}{TP+TN+FP+FN}=\frac{1000+47000}{50000}=\frac{48000}{50000}=\mathbf{0.96\ (96\%)}$$

$$\text{Precision}=\frac{TP}{TP+FP}=\frac{1000}{1000+1000}=\mathbf{0.50}$$

$$\text{Recall}=\frac{TP}{TP+FN}=\frac{1000}{1000+1000}=0.50$$

$$F_1=\frac{2\,\text{Precision}\times\text{Recall}}{\text{Precision}+\text{Recall}}=\frac{2(0.5)(0.5)}{0.5+0.5}=\mathbf{0.50}$$

```figure caption="Confusion matrix of the 50 000 test cases (counts). The huge No/No cell dominates, which is why accuracy looks excellent while the positive class is handled poorly."
import numpy as np
cm=np.array([[1000,1000],[1000,47000]])
fig,ax=plt.subplots(figsize=(4.2,3.2))
im=ax.imshow(np.log10(cm),cmap="Blues",vmin=2.5,vmax=5.2)
for i in range(2):
    for j in range(2):
        ax.text(j,i,["TP","FN","FP","TN"][2*i+j]+"\n"+format(cm[i,j],","),ha="center",va="center",fontsize=10,color="white" if cm[i,j]>10000 else INK)
ax.set_xticks([0,1]); ax.set_xticklabels(["Yes","No"]); ax.set_yticks([0,1]); ax.set_yticklabels(["Yes","No"])
ax.set_xlabel("Predicted class"); ax.set_ylabel("Actual class")
ax.set_title("Accuracy 0.96, Precision 0.50, F1 0.50",fontsize=9)
```

**(ii) Accuracy versus $F_1$.** Accuracy is $96\%$ but $F_1$ is only $0.50$. The data are **highly imbalanced**: only $2000$ of the $50\,000$ cases ($4\%$) are positive. A model that always predicts "No" would score $\frac{48000}{50000}=96\%$ accuracy too (the same figure as this model!), yet would find no positive at all. Accuracy is dominated by the large true-negative count $TN=47000$, so it hides the poor performance on the minority (positive) class: the model finds only half of the real positives (recall $0.5$) and half of its "Yes" predictions are wrong (precision $0.5$). $F_1$, the harmonic mean of precision and recall, ignores $TN$ and therefore reveals this weakness. For imbalanced problems (fraud, disease, spam) $F_1$ (or precision / recall / PR-AUC) is the right measure, not accuracy.

@s 3
**(a) Central Limit Theorem (CLT).**

*Statement.* Let $X_1,X_2,\dots,X_n$ be independent, identically distributed random variables with finite mean $\mu$ and finite variance $\sigma^2$ (the distribution of $X$ can be of any shape). Then the sample mean $\bar X=\frac1n\sum X_i$ satisfies

$$\begin{gathered}\bar X\ \approx\ N\!\left(\mu,\ \frac{\sigma^2}{n}\right) \\ Z=\frac{\bar X-\mu}{\sigma/\sqrt n}\ \xrightarrow[n\to\infty]{}\ N(0,1).\end{gathered}$$

The approximation is usually good for $n\ge30$ (earlier when the population is nearly symmetric). The standard deviation of the sample mean, $\sigma/\sqrt n$, is called the **standard error**.

```figure caption="CLT demonstration: means of samples drawn from a very skewed (exponential) population. As n grows the distribution of the sample mean becomes bell shaped and narrower (SE = sigma / sqrt n)."
import numpy as np
rng=np.random.default_rng(7)
fig,ax=plt.subplots(1,4,figsize=(7.4,2.3),sharey=False)
pop=rng.exponential(1.0,20000)
ax[0].hist(pop,bins=40,color="#9fb8d9",ec="white"); ax[0].set_title("population (skewed)",fontsize=7.5)
for a,n in zip(ax[1:],[2,10,50]):
    m=rng.exponential(1.0,(8000,n)).mean(axis=1)
    a.hist(m,bins=40,color=ACCENT,ec="white",density=True)
    xs=np.linspace(m.min(),m.max(),200); a.plot(xs,np.exp(-(xs-1)**2/(2/n))/np.sqrt(2*np.pi/n),color="#c62828",lw=1.2)
    a.set_title("means of n = %d"%n,fontsize=7.5)
for a in ax: a.tick_params(labelsize=6.5)
plt.tight_layout()
```

*Why it is important in data analysis.*

- It lets us use the **normal distribution** for the sample mean even when the population is not normal, so we do not have to know the population distribution.
- It is the basis of **confidence intervals** ($\bar x\pm z\,\sigma/\sqrt n$) and **hypothesis tests** (z-test, t-test, A/B testing).
- It explains why averages of many small independent effects (measurement errors, noise) look Gaussian, so Gaussian noise models are reasonable.
- It tells how the precision grows with the sample size: the error falls as $1/\sqrt n$ (four times the data halves the error), which guides **sample-size planning** and survey design.
- It justifies bootstrapping, Monte-Carlo estimation and the averaging of stochastic gradients / ensemble predictions in machine learning.

**(b) E-mail spam filter (Bayes' theorem).** Let $S$ = spam, $V$ = valid, $F$ = contains the word "free". Given $P(S)=0.25$, so $P(V)=0.75$; $P(F\mid S)=0.70$; $P(F\mid V)=0.04$.

**(i) Total probability that a message contains "free":**

$$P(F)=P(F\mid S)P(S)+P(F\mid V)P(V)=0.70(0.25)+0.04(0.75)=0.175+0.030=\mathbf{0.205}$$

**(ii) Spam given that it contains "free" (Bayes):**

$$P(S\mid F)=\frac{P(F\mid S)P(S)}{P(F)}=\frac{0.175}{0.205}=\frac{35}{41}=\mathbf{0.8537\ (\approx85.4\%)}$$

**(iii) Valid given that it does not contain "free":** $P(\bar F\mid V)=1-0.04=0.96$, $P(\bar F\mid S)=0.30$, $P(\bar F)=1-0.205=0.795$. (Check: $0.30\times0.25+0.96\times0.75=0.075+0.72=0.795$.)

$$P(V\mid\bar F)=\frac{P(\bar F\mid V)P(V)}{P(\bar F)}=\frac{0.96\times0.75}{0.795}=\frac{0.72}{0.795}=\mathbf{0.9057\ (\approx90.6\%)}$$

So a message containing "free" is spam with about $85\%$ probability, while a message without it is valid with about $91\%$ probability.

@s 4
**(a) Data structure types.**

- **Structured data** follows a fixed, predefined schema of rows and columns with typed fields: relational tables, spreadsheets, CSV. It is queried with SQL. Example: a student table (roll_no, name, marks).
- **Unstructured data** has no predefined model or schema: free text, images, audio, video, PDFs, e-mails. It needs special processing (NLP, computer vision) to extract information. About 80% of the world's data is of this kind.
- **Semi-structured data** has **no rigid table schema but carries tags, keys or markers that separate and label elements and give a hierarchy**: JSON, XML, HTML, YAML, log files, NoSQL (document) records, e-mail (headers + free body). Different records may have different fields, and fields may be nested.

| | Structured | Semi-structured | Unstructured |
|---|---|---|---|
| Schema | fixed, defined before storing | flexible, self-describing (tags / keys) | none |
| Format | tables, CSV | JSON, XML, HTML, logs | text, image, audio, video |
| Storage | RDBMS | document / key-value NoSQL, files | data lake, object store |
| Query | SQL | JSONPath, XPath, MongoDB queries | search, ML / NLP / CV |
| Ease of analysis | easiest | moderate | hardest |

Example of semi-structured data (JSON): `{"name":"Sita","courses":["DS","OS"],"address":{"city":"Pokhara"}}` and another record `{"name":"Ram","phone":"98xxxxxxx"}`: the two records have different fields yet each is self-describing.

**(b) Handling missing data.** Missing values (NaN / null / blank) arise from non-response, sensor failure or entry errors; most algorithms cannot accept them. First, find the pattern (random or not) and the percentage missing. Two common methods:

**Method 1: Deletion (listwise / drop).** Drop the records (or a column if it is mostly empty). It is simple but loses data and can bias the result; used only when few values are missing, completely at random.

**Method 2: Imputation.** Fill the missing entry with a sensible value: the **mean** (numerical, symmetric data), the **median** (skewed data or outliers), the **mode** (categorical), or a model-based estimate (KNN or regression imputation, forward-fill for time series).

*Example.* Ages of 7 customers: $22,\ 25,\ ?,\ 30,\ 28,\ ?,\ 26$.

| ID | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Age (raw) | 22 | 25 | NaN | 30 | 28 | NaN | 26 |
| After deletion (drop rows 3, 6) | 22 | 25 | | 30 | 28 | | 26 |
| After mean imputation | 22 | 25 | 26.2 | 30 | 28 | 26.2 | 26 |
| After median imputation | 22 | 25 | 26 | 30 | 28 | 26 | 26 |

Deletion leaves $5$ rows ($29\%$ of the data lost). The mean of the $5$ known values is $\frac{22+25+30+28+26}{5}=\frac{131}{5}=26.2$ and the median is $26$; replacing both NaN by $26.2$ keeps all $7$ rows and preserves the mean (but slightly shrinks the variance). In pandas: `df.dropna()` and `df['age'].fillna(df['age'].mean())`.

@s 5
All ten ages as one sample: $23,\,23,\,24,\,25,\,28,\,29,\,29,\,32,\,35,\,36$ (sorted), $n=10$. Women: $35,29,32,23,36$; men: $28,25,29,24,23$.

**(a) Normalisation of Data #1.** Women's age $x=35$, men's age $x=28$.

*Mean:* $\bar x=\dfrac{35+29+32+23+36+28+25+29+24+23}{10}=\dfrac{284}{10}=28.4$.

*Deviations squared:* $(35-28.4)^2=43.56$, $(29-28.4)^2=0.36$, $(32-28.4)^2=12.96$, $(23-28.4)^2=29.16$, $(36-28.4)^2=57.76$, $(28-28.4)^2=0.16$, $(25-28.4)^2=11.56$, $(29-28.4)^2=0.36$, $(24-28.4)^2=19.36$, $(23-28.4)^2=29.16$. Their sum is $\sum(x-\bar x)^2=204.4$.

Sample standard deviation: $s=\sqrt{\dfrac{204.4}{10-1}}=\sqrt{22.711}=4.7656$ (population value $\sigma=\sqrt{204.4/10}=4.5211$).

**z-score** $z=\dfrac{x-\bar x}{s}$:

$$\begin{gathered}z_{\text{woman}}=\frac{35-28.4}{4.7656}=\frac{6.6}{4.7656}=\mathbf{1.385} \\ z_{\text{man}}=\frac{28-28.4}{4.7656}=\frac{-0.4}{4.7656}=\mathbf{-0.084}\end{gathered}$$

(With the population $\sigma=4.5211$ the values are $1.460$ and $-0.088$.) The woman is about $1.4$ standard deviations above the class mean age; the man is almost exactly at the mean.

**Min-max (zero-to-one)** $x'=\dfrac{x-x_{\min}}{x_{\max}-x_{\min}}$ with $x_{\min}=23$, $x_{\max}=36$ (range $13$):

$$\begin{gathered}x'_{\text{woman}}=\frac{35-23}{13}=\frac{12}{13}=\mathbf{0.923} \\ x'_{\text{man}}=\frac{28-23}{13}=\frac{5}{13}=\mathbf{0.385}\end{gathered}$$

**(b) Box plot of all 10 ages.** Sorted data: $23, 23, 24, 25, 28, 29, 29, 32, 35, 36$.

- **Minimum** $=23$, **maximum** $=36$.
- **Median** (average of the 5th and 6th values) $Q_2=\dfrac{28+29}{2}=28.5$.
- **Lower quartile** $Q_1$ = median of the lower half $(23,23,24,25,28)$ $=24$.
- **Upper quartile** $Q_3$ = median of the upper half $(29,29,32,35,36)$ $=32$.
- **IQR** $=Q_3-Q_1=32-24=8$.
- **Fences:** lower $=Q_1-1.5\,\text{IQR}=24-12=12$; upper $=Q_3+1.5\,\text{IQR}=32+12=44$. All data lie inside $[12,44]$, so there are **no outliers**; the whiskers reach the minimum $23$ and the maximum $36$.

(If the interpolation method of software such as NumPy is used, $Q_1=24.25$, $Q_3=31.25$; the picture is practically the same.)

```figure caption="Box plot of the ten student ages: min 23, Q1 24, median 28.5, Q3 32, max 36 (IQR 8, no outliers). The dot marks the mean 28.4."
import numpy as np
d=[35,29,32,23,36,28,25,29,24,23]
fig,ax=plt.subplots(figsize=(6.6,2.7))
ax.boxplot(d,vert=False,whis=1.5,widths=0.5,patch_artist=True,boxprops=dict(facecolor="#cfe3ff",edgecolor=INK,lw=1.3),medianprops=dict(color="#c62828",lw=2),whiskerprops=dict(color=INK,lw=1.3),capprops=dict(color=INK,lw=1.3))
ax.plot([28.4],[1],"o",color=ACCENT,ms=6,label="mean 28.4")
ax.set_ylim(0.4,1.9); ax.set_yticks([]); ax.set_xlim(20,40)
for x,t,y in [(23,"min 23",1.38),(24,"Q1 = 24",0.63),(28.5,"median = 28.5",1.38),(32,"Q3 = 32",0.63),(36,"max 36",1.38)]:
    ax.annotate(t,(x,1.0),(x,y),ha="center",fontsize=8,arrowprops=dict(arrowstyle="-",color="#888",lw=0.7))
ax.set_xlabel("Age of student (years)"); ax.set_title("Box plot of the age of 10 graduate students",fontsize=9); ax.legend(loc="upper right",fontsize=7,frameon=False)
```

@s 6
**(a) Purposes of data visualization.**

1. **Exploration:** see the shape of the data (distribution, trend, clusters, outliers, missing values) before modelling (histogram, scatter plot, box plot).
2. **Finding patterns and relationships:** correlations, seasonality, comparisons between groups.
3. **Communication / storytelling:** present findings so managers and the public understand and trust them (dashboards, infographics).
4. **Decision support and monitoring:** track KPIs in real time and spot anomalies quickly.
5. **Validation and diagnosis of models:** residual plots, ROC curves, confusion matrices, learning curves.
6. **Memory and efficiency:** humans grasp pictures much faster than tables of numbers; a good chart compresses thousands of values.

**Heat map.** A heat map shows a *matrix* of values as a grid of coloured cells; the colour (intensity or hue) encodes the magnitude, so high and low regions are noticed at once. Typical uses: a **correlation matrix** between features (used in feature selection), a confusion matrix, website click density, gene expression, or the number of customers by hour and weekday.

*Example.* Number of customers in a shop by day and time slot:

| | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| 8-12 | 20 | 22 | 25 | 24 | 30 | 45 | 40 |
| 12-16 | 35 | 33 | 38 | 36 | 44 | 70 | 66 |
| 16-20 | 50 | 52 | 55 | 58 | 75 | 95 | 90 |

```figure caption="Heat map of customers by weekday and time slot: the dark cells (Friday to Sunday, 16-20 h) show the peak demand, which tells the manager when to schedule extra staff."
import numpy as np
M=np.array([[20,22,25,24,30,45,40],[35,33,38,36,44,70,66],[50,52,55,58,75,95,90]])
fig,ax=plt.subplots(figsize=(6.2,2.6))
im=ax.imshow(M,cmap="YlOrRd",aspect="auto")
ax.set_xticks(range(7)); ax.set_xticklabels(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],fontsize=8)
ax.set_yticks(range(3)); ax.set_yticklabels(["8-12","12-16","16-20"],fontsize=8)
for i in range(3):
    for j in range(7): ax.text(j,i,M[i,j],ha="center",va="center",fontsize=8,color="white" if M[i,j]>70 else INK)
plt.colorbar(im,ax=ax,label="customers",fraction=0.04)
ax.set_title("Customer traffic heat map",fontsize=9)
```

Reading: demand rises from morning to evening and from weekday to weekend, with the maximum of $95$ on Saturday evening. Libraries: `seaborn.heatmap(df.corr(), annot=True, cmap='coolwarm')`.

**(b) Regression.** Regression is a supervised-learning / statistical technique that models the relationship between a **dependent (target) variable** $y$ and one or more **independent (predictor) variables** $x$, so that a **continuous** value can be estimated for new inputs. The simple linear model is $y=\beta_0+\beta_1x+\varepsilon$; the coefficients are found by **least squares**, minimising $\sum(y_i-\hat y_i)^2$:

$$\begin{gathered}\beta_1=\frac{\sum(x_i-\bar x)(y_i-\bar y)}{\sum(x_i-\bar x)^2} \\ \beta_0=\bar y-\beta_1\bar x .\end{gathered}$$

*Support for predictive analytics.* The fitted equation (i) **predicts** the outcome for unseen inputs (forecasting), (ii) **quantifies** the effect of each factor (the slope), (iii) measures the fit by $R^2$ and the error (MAE, RMSE), and (iv) lets "what-if" analysis be done for planning. Variants: multiple, polynomial, ridge / lasso regression (logistic regression is used for classification).

*Business application: advertising and sales.* A shop owner records monthly advertising spend $x$ (in Rs. thousand) and sales $y$ (in Rs. lakh):

| $x$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $y$ | 12 | 15 | 21 | 24 | 28 |

$\bar x=3$, $\bar y=20$, $\sum(x-\bar x)(y-\bar y)=(-2)(-8)+(-1)(-5)+0+(1)(4)+(2)(8)=41$, $\sum(x-\bar x)^2=10$. So $\beta_1=4.1$, $\beta_0=20-4.1\times3=7.7$:

$$\begin{gathered}\hat y=7.7+4.1\,x \\ R^2=0.989 .\end{gathered}$$

Interpretation: with no advertising the sales are about Rs. $7.7$ lakh, and every extra Rs. 1000 of advertising adds about Rs. $4.1$ lakh of sales. **Prediction:** a spend of $x=6$ gives $\hat y=7.7+4.1(6)=\mathbf{32.3}$ lakh, which helps to set the budget.

```figure caption="Linear regression of sales on advertising spend: fitted line y = 7.7 + 4.1x (R^2 = 0.989) and the predicted sales for a spend of 6."
import numpy as np
x=np.array([1,2,3,4,5]); y=np.array([12,15,21,24,28])
fig,ax=plt.subplots(figsize=(5.4,3.0))
xs=np.linspace(0.5,6.5,10); ax.plot(xs,7.7+4.1*xs,color=ACCENT,lw=1.8,label="$\\hat y=7.7+4.1x$")
ax.scatter(x,y,color="#c62828",zorder=3,label="observed data")
ax.vlines(x,y,7.7+4.1*x,color="#999",lw=0.8,ls=":")
ax.scatter([6],[32.3],marker="*",s=140,color="#2e7d32",zorder=4,label="prediction (6, 32.3)")
ax.set_xlabel("advertising spend x (Rs. thousand)"); ax.set_ylabel("sales y (Rs. lakh)"); ax.legend(fontsize=7.5,frameon=False); ax.grid(alpha=0.25)
```

@s 7
Any three are answered; all four are given.

**(i) GDPR (General Data Protection Regulation).** A European Union law (in force since 25 May 2018) that protects the personal data and privacy of people in the EU/EEA. It applies to **any organisation, anywhere in the world**, that collects or processes the data of EU residents. Main principles: lawfulness, fairness and transparency; **purpose limitation**; **data minimisation**; accuracy; storage limitation; integrity and confidentiality; accountability. Rights of the data subject: access, rectification, **erasure ("right to be forgotten")**, restriction, data portability, objection to profiling and automated decisions. Duties of organisations: obtain clear **consent**, privacy by design, appoint a data protection officer where needed, and report a breach within **72 hours**. Fines go up to **EUR 20 million or 4% of global annual turnover**, whichever is higher. For data scientists it means anonymising or pseudonymising data, documenting the lawful basis and being able to explain automated decisions.

**(ii) Feature selection.** The process of choosing the most relevant subset of the input variables for building a model and discarding irrelevant or redundant ones. *Benefits:* less over-fitting, better accuracy, shorter training time, simpler and more interpretable models, and lower storage and data-collection cost (it counters the curse of dimensionality). *Methods:*

- **Filter methods** use a statistic independent of the model: correlation, chi-square test, ANOVA F-test, mutual information, variance threshold.
- **Wrapper methods** train the model on subsets and keep the best: forward selection, backward elimination, recursive feature elimination (RFE).
- **Embedded methods** select features during training: LASSO ($L_1$ penalty shrinks coefficients to zero), decision-tree / random-forest importance.

(It differs from feature *extraction* such as PCA, which creates new features.) Example: from {age, income, id, height} to predict loan default, the row id is dropped because it carries no information, and one of two highly correlated columns is removed.

**(iii) Generative AI.** Artificial intelligence models that **learn the distribution of the training data and generate new content** (text, images, audio, video, code, molecules) that resembles it, instead of only classifying or predicting. Main model families: **large language models** based on the Transformer (GPT, Gemini, LLaMA), **diffusion models** (Stable Diffusion, DALL-E), **GANs** (a generator and a discriminator trained against each other), and **VAEs**. They are pre-trained on huge corpora by self-supervised learning (e.g., next-token prediction) and then fine-tuned, aligned with human feedback (RLHF) or guided by prompts and retrieval (RAG). *Applications:* chatbots and assistants, code generation, translation and summarisation, image / music creation, synthetic data for training, drug design. *Concerns:* hallucination (confident wrong output), bias, copyright and privacy, deepfakes and misinformation, high energy cost; hence human oversight and evaluation are required.

**(iv) Performance measure using MAE.** The **Mean Absolute Error** is the standard error measure for regression models:

$$\text{MAE}=\frac1n\sum_{i=1}^{n}\lvert y_i-\hat y_i\rvert ,$$

the average size of the prediction error, in the **same unit as the target**. It treats all errors linearly, so it is **robust to outliers** (unlike MSE / RMSE, which square the errors and penalise large errors more) and is easy to interpret ("on average the forecast is wrong by MAE units"). A smaller value is better, and $0$ is a perfect fit. Its drawbacks: it is not differentiable at $0$ (harder to optimise directly) and does not show whether the model over- or under-predicts (the sign is lost).

*Example.* Actual $y=(10,12,15,20,8)$, predicted $\hat y=(11,10,18,19,8)$. Absolute errors: $1,2,3,1,0$.

$$\begin{gathered}\text{MAE}=\frac{1+2+3+1+0}{5}=\frac75=\mathbf{1.4}\ \text{units} \\ \text{RMSE}=\sqrt{\frac{1+4+9+1+0}{5}}=\sqrt3=1.73 .\end{gathered}$$

RMSE $>$ MAE because it penalises the error of $3$ more heavily. In scikit-learn: `mean_absolute_error(y_true, y_pred)`.
