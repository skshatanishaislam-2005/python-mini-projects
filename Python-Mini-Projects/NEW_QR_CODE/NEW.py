from urllib.parse import quote
import qrcode

upi_id = input("Enter your UPI ID: ")
name = input("Enter Recipient Name: ")
message = "Thank You From Tanisha❤️, LOVE UUUU🥹 For Giving Me Your Money🤑😘💸"

encoded_name = quote(name)
encoded_message = quote(message)

# Each app has its own deep link scheme
phonepe_url = f'upi://pay?pa={upi_id}&pn={encoded_name}&tn={encoded_message}&cu=INR'
paytm_url   = f'paytmmp://pay?pa={upi_id}&pn={encoded_name}&tn={encoded_message}&cu=INR'
gpay_url    = f'tez://upi/pay?pa={upi_id}&pn={encoded_name}&tn={encoded_message}&cu=INR'

apps = {
    'phonepe': phonepe_url,
    'paytm':   paytm_url,
    'gpay':    gpay_url,
}

for app_name, url in apps.items():
    qr = qrcode.make(url)
    filename = f'{app_name}_qr.png'
    qr.save(filename)
    print(f"Saved: {filename}")
    qr.show()

