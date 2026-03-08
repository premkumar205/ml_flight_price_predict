# ✈️ Flight Price Prediction App

A machine learning web application that predicts flight prices based on various factors like airline, route, travel date, and time.

## 🎯 Features

- **Real-time Price Prediction** - Get instant flight price estimates
- **User-Friendly Interface** - Easy-to-use Streamlit web interface
- **Multiple Airlines Support** - IndiGo, Air India, SpiceJet, and more
- **Flexible Route Selection** - Choose source, destination, and stops
- **Time Picker Interface** - Simplified time selection for departures and arrivals

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## 🚀 Installation & Setup

### Local Setup

1. **Clone or download the project**
```bash
cd flight_price_prediction
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
flight_price_prediction/
├── app.py                    # Main Streamlit application
├── flight_model.keras        # Trained neural network model
├── label_encoders.pkl        # Scikit-learn label encoders
├── feature_columns.pkl       # Feature column names
├── Data_Train.xlsx          # Training dataset
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 How It Works

1. **Data Input** - User provides flight details (airline, route, date, time)
2. **Preprocessing** - Input data is cleaned and transformed to match training format
3. **Prediction** - Neural network predicts the flight price
4. **Output** - Estimated price is displayed to the user

## 📊 Model Details

- **Algorithm**: Deep Neural Network (Keras/TensorFlow)
- **Architecture**: 4 hidden layers with ReLU activation
- **Training Data**: 10,682 flight records
- **Features**: 20 input features after preprocessing
- **Performance**: Trained to minimize MAE and MSE

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free)

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" and select your repository
4. Set main file path to `app.py`
5. Deploy!

**Required for GitHub:**
- Copy entire project folder to GitHub
- Ensure `requirements.txt` is present

### Option 2: Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run app.py --logger.level=error" > Procfile

# Deploy
heroku login
heroku create your-app-name
git push heroku main
```

### Option 3: AWS/Azure/Google Cloud

Use their container deployment services with the included dependencies.

## 📝 Usage Example

1. Select your preferred airline (IndiGo, Air India, etc.)
2. Choose source and destination cities
3. Set journey date and flight times using the time picker
4. Specify flight duration and total stops
5. Click "💰 Predict Flight Price"
6. View the estimated price in Indian Rupees (₹)

## ⚙️ Configuration

All settings are in `app.py`. Key configurations:

- **Default Values**: Journey date (June 15, 2019), Departure (10:30 AM), Arrival (3:45 PM)
- **Date Range**: 2018-2025
- **Duration**: 0-1440 minutes (0-24 hours)
- **Model**: `flight_model.keras` (loaded from disk)

## 🐛 Troubleshooting

### Model loading error
- Ensure `flight_model.keras` exists in the project directory
- Verify TensorFlow is installed: `pip install tensorflow`

### Missing columns
- Verify `feature_columns.pkl` is present
- Ensure `label_encoders.pkl` is in the directory

### Data loading error
- Check that `Data_Train.xlsx` exists
- Ensure Excel file is not corrupted

## 📈 Future Improvements

- Add more airlines and routes
- Implement price history visualization
- Add booking integration
- Multi-language support
- Mobile app version

## 📄 License

This project is free to use for educational purposes.

## 👨‍💼 Support

For issues or questions, please check the code comments or review the preprocessing functions in `app.py`.

---

**Built with**: Python, Streamlit, TensorFlow, Scikit-learn, Pandas
