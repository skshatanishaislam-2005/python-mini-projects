# 💸 UPI QR Code Generator

Generate UPI payment QR codes for **PhonePe**, **Paytm**, and **Google Pay** — all at once, with a custom thank-you message baked right in.



## 📋 What It Does

This script takes a UPI ID and recipient name as input and generates three separate QR code images — one for each major UPI payment app. Each QR encodes a deep link that pre-fills the payment details so the payer just scans and pays.



## 🗂️ Files Generated

| File | App |
|------|-----|
| `phonepe_qr.png` | PhonePe |
| `paytm_qr.png` | Paytm |
| `gpay_qr.png` | Google Pay |



## ⚙️ Requirements

**Python 3.x** and the following library:

```bash
pip install qrcode[pil]
```

> `urllib.parse` is part of Python's standard library — no install needed.

---

## 🚀 How to Run

```bash
python upi_qr_generator.py
```

You'll be prompted to enter:

```
Enter your UPI ID:       → e.g. tanisha@upi
Enter Recipient Name:    → e.g. Tanisha
```

The script will save the three QR images in the current directory and open a preview of each.



## 🔗 UPI Deep Link Format

Each app uses a slightly different deep link scheme:

| App | Scheme |
|-----|--------|
| PhonePe | `upi://pay?...` |
| Paytm | `paytmmp://pay?...` |
| Google Pay | `tez://upi/pay?...` |

All links include:
- `pa` — Payee UPI ID
- `pn` — Payee Name
- `tn` — Transaction Note (your custom message)
- `cu` — Currency (`INR`)

---

## 💬 Custom Message

The transaction note is hardcoded as:

```
Thank You From Tanisha❤️, LOVE UUUU🥹 For Giving Me Your Money🤑😘💸
```

To change it, edit the `message` variable in the script.

---

## 📌 Notes

- QR codes work best when scanned from a printed sheet or a phone screen.
- The deep links trigger the respective app if installed; behavior may vary by device.
- Amount is intentionally left blank — the payer enters it themselves.

---

## 🛠️ Possible Improvements

- [ ] Add an `amount` input parameter to pre-fill the payment amount
- [ ] Bundle all three QR codes into a single image or PDF
- [ ] Build a simple GUI using `tkinter`
- [ ] Add a CLI flag to customize the thank-you message

---

## Author
Tanisha