# 💸 UPI QR Code Generator (Simplified)

A lightweight Python script that generates UPI payment QR codes for **PhonePe**, **Paytm**, and **Google Pay** using a single standard UPI deep link.

---

## 📋 What It Does

Enter your UPI ID once — the script generates three QR code images, one per app, each encoding the same `upi://pay` link with a sweet little message attached.

---

## 🗂️ Files Generated

| File | App |
|------|-----|
| `phonepe_qr.png` | PhonePe |
| `paytm_qr.png` | Paytm |
| `google_pay_qr.png` | Google Pay |

---

## ⚙️ Requirements

**Python 3.x** + one library:

```bash
pip install qrcode[pil]
```

---

## 🚀 How to Run

```bash
python upi_qr_generator.py
```

You'll be prompted for:

```
Enter your UPI ID = your@upi
```

The three QR images are saved in the current directory and auto-previewed.

---

## 🔗 UPI Link Format Used

All three QRs use the standard `upi://` scheme:

```
upi://pay?pa=<UPI_ID>&pn=Recipient%20Name&tn=Love%20You%20From%20Tanisha%E2%9D%A4%EF%B8%8F%F0%9F%92%B8
```

| Parameter | Value |
|-----------|-------|
| `pa` | Your UPI ID (from input) |
| `pn` | `Recipient Name` (hardcoded placeholder) |
| `tn` | `Love You From Tanisha❤️💸` |

> **Note:** All three QR codes currently encode the same URL — they differ only in filename. To use app-specific deep links (e.g. `tez://` for GPay, `paytmmp://` for Paytm), see the improvements section below.

---

## 💬 Custom Message

The transaction note is set as:

```
Love You From Tanisha❤️💸
```

To change it, edit the `message` line in the script:

```python
message = quote("Your custom message here")
```

---

## 📌 Notes

- No amount is pre-filled — the payer enters it themselves.
- QR codes work best when printed or displayed on a clear screen.
- The `upi://` scheme is universally supported across all UPI apps.

---

## 🛠️ Possible Improvements

- [ ] Accept recipient name as input instead of hardcoding it
- [ ] Add optional amount input (`&am=`)
- [ ] Use app-specific deep links for PhonePe (`upi://`), Paytm (`paytmmp://`), GPay (`tez://upi/pay`)
- [ ] Combine all three QRs into one image side-by-side
- [ ] Add a `tkinter` GUI for a friendlier interface

---

*Made with 💻 + ❤️ by Tanisha*
