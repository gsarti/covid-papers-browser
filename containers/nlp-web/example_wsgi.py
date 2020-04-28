from app import app

app.secret_key = 'I_AM_A_SUPER_MEGA_SECRET_KEY'
app.config['SESSION_PERMANENT']=False,
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
