import tkinter as tk
from tkinter import messagebox, ttk
import google.generativeai as genai

genai.configure(api_key="API_KEY")
model = genai.GenerativeModel('gemini-2.5-flash')

def get_gemini_recommendation():
    user_input = entry.get().lower().strip()
    age_group = age_var.get()
    
    if not user_input:
        return

    prompt = f"""
    You are a medical assistant tool. A user is reporting these symptoms: '{user_input}'.
    The patient is a/an {age_group}.
    
    Task:
    1. Suggest 2-3 common Indian Over-the-Counter (OTC) medicine brands (like Dolo, Digene, etc.).
    2. Specify if it should be a Tablet, Syrup, or Gel based on the age group ({age_group}).
    3. Keep the response extremely concise (bullet points).
    4. Do not suggest prescription-only antibiotics or heavy sedatives.
    """

    try:
        response = model.generate_content(prompt)
        
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, f"AI Suggestions for {age_group.capitalize()}:\n\n")
        result_text.insert(tk.END, response.text)
        result_text.config(state=tk.DISABLED)
        
    except Exception as e:
        messagebox.showerror("API Error", f"Could not connect to Gemini: {e}")

root = tk.Tk()
root.title("AI Health Assistant")
root.geometry("500x650")
root.configure(bg="#ffffff")

root.columnconfigure(0, weight=1)
root.rowconfigure(5, weight=1)

tk.Label(root, text="AI Medicine Finder (Gemini)", font=("Arial", 16, "bold"), bg="#ffffff").grid(row=0, column=0, pady=20)

age_frame = tk.Frame(root, bg="#ffffff")
age_frame.grid(row=1, column=0, pady=5)
age_var = tk.StringVar(value="adult")
tk.Radiobutton(age_frame, text="Adult", variable=age_var, value="adult", bg="#ffffff").pack(side=tk.LEFT, padx=15)
tk.Radiobutton(age_frame, text="Child", variable=age_var, value="child", bg="#ffffff").pack(side=tk.LEFT, padx=15)

entry = ttk.Entry(root, width=45)
entry.grid(row=2, column=0, pady=15)
entry.insert(0, "Describe symptoms (e.g., headache and body pain)")

search_btn = tk.Button(root, text="Ask Gemini AI", command=get_gemini_recommendation, bg="#000000", fg="#ffffff", width=20, relief="flat")
search_btn.grid(row=3, column=0, pady=10)

result_frame = tk.Frame(root, bg="#ffffff", highlightbackground="#eeeeee", highlightthickness=2)
result_frame.grid(row=4, column=0, padx=40, pady=20, sticky="nsew")

result_text = tk.Text(result_frame, font=("Arial", 10), bg="#ffffff", bd=0, state=tk.DISABLED, wrap=tk.WORD, height=12)
result_text.pack(fill="both", expand=True, padx=15, pady=15)

disclaimer_lbl = tk.Label(root, 
    text="Disclaimer: AI suggestions are for informational purposes only. Consult a doctor.",
    fg="#999999", bg="#ffffff", font=("Arial", 8))
disclaimer_lbl.grid(row=5, column=0, pady=10, sticky="s")

root.mainloop()