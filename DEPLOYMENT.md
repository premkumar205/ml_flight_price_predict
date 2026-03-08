# 🚀 Deployment Guide - Flight Price Predictor

## Quick Deployment (Streamlit Cloud - Recommended)

### Step 1: Prepare GitHub Repository

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit: Flight Price Prediction App"
```

### Step 2: Push to GitHub

1. Create a new GitHub repository at https://github.com/new
2. Name it `flight-price-predictor`
3. Push your code:

```bash
git remote add origin https://github.com/YOUR_USERNAME/flight-price-predictor.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **"New app"**
3. Fill in your details:
   - **Repository**: `YOUR_USERNAME/flight-price-predictor`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **"Deploy"** ✨

Your app will be live in ~2 minutes at: `https://flight-price-predictor.streamlit.app`

---

## Alternative: Deploy on Heroku

### Step 1: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Deploy

```bash
heroku login
heroku create your-unique-app-name
git push heroku main
heroku open
```

Your app will be live at: `https://your-unique-app-name.herokuapp.com`

---

## File Checklist Before Deployment

✅ Make sure these files exist:
- [ ] `app.py`
- [ ] `flight_model.keras`
- [ ] `label_encoders.pkl`
- [ ] `feature_columns.pkl`
- [ ] `Data_Train.xlsx`
- [ ] `requirements.txt`
- [ ] `README.md`
- [ ] `.gitignore`
- [ ] `.streamlit/config.toml`
- [ ] `Procfile` (if deploying to Heroku)

---

## Post-Deployment

### Test Your Deployed App

1. Open the deployed URL in your browser
2. Enter sample flight details:
   - **Airline**: IndiGo
   - **Source**: Bangalore
   - **Destination**: New Delhi
   - **Departure**: 10:30 AM
   - **Arrival**: 3:45 PM
   - **Duration**: 180 minutes
   - **Total Stops**: 0
3. Click **"Predict Flight Price"**
4. Verify the price prediction displays correctly

### Monitor Performance

- **Streamlit Cloud**: Dashboard at share.streamlit.io shows app logs
- **Heroku**: View logs with `heroku logs --tail`

---

## Troubleshooting Deployment

### "Module not found" error
```bash
# Regenerate requirements.txt with pinned versions
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Model file too large
If `flight_model.keras` is >100MB:
1. Use Git LFS: `git lfs install`
2. Track large files: `git lfs track "*.keras"`
3. Commit and push

### Memory issues on Heroku
Heroku free tier has 512MB RAM. If issues:
- Upgrade to paid tier
- Or use Streamlit Cloud (more generous)

---

## Environment Variables (Optional)

Create `.streamlit/secrets.toml` for sensitive data:

```toml
# Example (don't commit this file!)
database_url = "your_database_url"
api_key = "your_api_key"
```

Then in `app.py`:
```python
import streamlit as st
db_url = st.secrets["database_url"]
```

---

## Scaling for Production

For high traffic sites:

1. **Upgrade Streamlit Cloud**: Pro/Business plans
2. **Use GPU**: For faster predictions (Heroku Premium)
3. **Add caching**: Already implemented in app
4. **Database**: Store predictions for analytics
5. **Load testing**: Use Apache JMeter or Locust

---

## Success Checklist

- [ ] App deployed successfully
- [ ] App loads without errors
- [ ] Time picker works correctly
- [ ] Predictions vary by location/airline
- [ ] Prices are in reasonable range (₹5,000-₹50,000)
- [ ] No "constant prediction" issue

---

## Support

**Streamlit Cloud Issues**: https://docs.streamlit.io/

**Heroku Issues**: https://devcenter.heroku.com/

**TensorFlow Issues**: https://www.tensorflow.org/install

---

**Your app is now ready for production! 🎉**
