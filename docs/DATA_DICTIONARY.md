# Data Dictionary

Full column reference for `data/03_features/ecommerce_customers_features.csv` (the final analytical dataset). See `data/01_raw/data_dictionary.csv` for a CSV version of the raw-column subset.

## Raw Columns (30)

| Column | Type | Description |
|--------|------|--------------|
| `customer_id` | string | Unique customer identifier (`ECO-XXXXX`) |
| `age` | int | Customer age in years (18–72) |
| `gender` | string | Gender identity |
| `country` | string | Customer country (12 countries) |
| `region` | string | World region grouping |
| `annual_income` | int | Annual income, USD |
| `total_spend` | int | Total lifetime spend, USD |
| `num_orders` | int | Total orders placed |
| `avg_order_value` | float | Average value per order, USD |
| `preferred_category` | string | Most purchased product category |
| `acquisition_channel` | string | Channel through which customer was acquired |
| `payment_method` | string | Preferred payment method |
| `device_type` | string | Primary shopping device |
| `customer_segment` | string | RFM-style segment (Champion, Loyal, At-Risk, etc.) |
| `satisfaction_score` | float | CSAT score, 1–5 |
| `days_since_last_order` | int | Recency in days |
| `churn_risk` | int | Binary churn label (1 = at risk) |
| `loyalty_points` | int | Accumulated reward points |
| `email_open_rate` | float | Email campaign open rate, 0–1 |
| `return_rate` | float | Order return rate, 0–1 |
| `referral_count` | int | Referrals made |
| `account_age_days` | int | Days since account creation |
| `avg_session_duration_sec` | int | Avg browsing session length, seconds |
| `pages_per_session` | int | Avg pages viewed per session |
| `cart_abandonment_rate` | float | Cart abandonment rate, 0–1 |
| `discount_usage_rate` | float | Discount/promo usage rate, 0–1 |
| `reviews_submitted` | int | Product reviews written |
| `wishlist_items` | int | Items in wishlist |
| `mobile_app_user` | int | Uses mobile app (1 = yes) |
| `newsletter_subscriber` | int | Subscribed to newsletter (1 = yes) |

## Engineered Columns (11)

| Column | Formula / Logic | Purpose |
|--------|------------------|---------|
| `clv_score` | `spend × (csat/5) × (1 − return_rate)` | Lifetime-value proxy weighted by satisfaction & returns |
| `engagement_score` | weighted blend of email, orders, referrals, reviews, pages, newsletter | Composite engagement index (0–1) |
| `spend_to_income_ratio` | `spend / income` | Wallet-share indicator |
| `recency_score` | `1 − days_since_last_order/400` | Normalised recency (0–1, higher = more recent) |
| `digital_maturity_score` | blend of app usage, pages/session, newsletter | Digital channel sophistication |
| `rfm_score` | weighted blend of recency, frequency, monetary | Composite RFM score (0–1) |
| `value_tier` | quintile of `clv_score` | Bronze → Diamond |
| `income_bracket` | quartile of `annual_income` | Low / Mid / High / Premium |
| `age_group` | binned `age` | Gen Z / Millennial / Gen X / Boomer / Senior |
| `tenure_tier` | binned `account_age_days` | <3mo → 4yr+ |
| `session_depth` | binned `avg_session_duration_sec` | Bouncer / Browser / Explorer / Power User |
| `cluster` | K-Means (k=4) on behavioural features | Unsupervised customer archetype |
