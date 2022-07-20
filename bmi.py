from tkinter import *
from tkinter.messagebox import *
import mysql.connector 
import datetime
import pandas as pd

con  = None
splash = Tk()
splash.geometry("800x500+0+0")
splash.title("BMI Calculator")
sf = ("Arial",60,"bold")
sl = Label(splash,text = "BMI Calculator!",font = sf, fg = "red")
sl.pack(pady = 180)
me = 0
d = datetime.datetime.now()
g = ""
if d.hour<12:
	g = "Good Morning!"
elif d.hour<17:
	g = "Good Afternoon!"
else:
	g = "Good Evening!"
dt = str(d)+"\n"+ g
def menu():
	splash.destroy()
	def c1():
		cal_win.deiconify()
		menu.withdraw()
	def his():
		his_win.deiconify()
		menu.withdraw()
	def refresh1():
		db = mysql.connector.connect(host = "localhost",user = "root",password = "abc456",database = "bmi")
		cursor = db.cursor()
		cursor.execute("select count(*) from rec")
		result = cursor.fetchone()
		count_lbl.config(text ="Count = "+str(result[0]) ,font = font1)
	def export():
		con = None
		try:
			con = mysql.connector.connect(host = "localhost", user ="root", password = "abc456", database = "bmi",auth_plugin='mysql_native_password')
			print("Connected! exporting...")
			cursor = con.cursor()
			sql = "select * from rec"
			cursor.execute(sql)
			data = cursor.fetchall()
			df = pd.DataFrame(data,columns = ["Id","Name","Age","Phone","Gender","BMI"])
			df.to_csv("bmi_data_export.csv")
			con.commit()
		except Exception as e:
			print("issue",e)
		finally:
			if con is not None:
				con.close()
				print("Disconnected!")
	menu = Tk()
	menu.geometry("800x500+0+0")
	menu.title("BMI Calculator")
	menu.configure(background = '#ADD8E6')
	db = mysql.connector.connect(host = "localhost",user = "root",password = "abc456",database = "bmi")
	cursor = db.cursor()
	cursor.execute("select count(*) from rec")
	result = cursor.fetchone()
	font1 = ("Arial",20,"bold")
	font2 = ("Arial",20)
	greet = Label(menu,text = dt, font = font1)
	greet.pack(pady = 10)
	cal_but = Button(menu, text = "Calculate BMI", bd = 2, font = font1, command = c1)
	cal_but.pack(pady = 10)
	his_but = Button(menu, text = "View History", bd = 2, font = font1,command = his)
	his_but.pack(pady = 10)
	exp_but = Button(menu, text = "Export Data", bd = 2, font = font1,command = export)
	exp_but.pack(pady = 10)
	refr = Button(menu, text = "Refresh Count", bd = 2, font = font1,command = refresh1)
	refr.pack(pady = 10)
	count_lbl = Label(menu,text ="Count = "+str(result[0]) ,font = font1)
	count_lbl.pack(pady = 10)
	
	def c2():
		con_win.deiconify()
		cal_win.withdraw()
	def c3():
		menu.deiconify()
		cal_win.withdraw()
	def calculate():
		con = None
		try:
			con = mysql.connector.connect(host = "localhost", user ="root", password = "abc456", database = "bmi",auth_plugin='mysql_native_password')
			print("Connected!")
			cursor = con.cursor()
			sql = "insert into rec(name,age,phone,gender,bmi) values('%s','%d','%d','%s','%d')"
			n = cal_win_nm_ent.get()
			if not n.isalpha():
				showerror("Error","Invalid Name: Enter Alphabets")
				cal_win_nm_ent.delete(0,END)
				cal_win_nm_ent.focus()
				return
			elif len(n)<2:
				showerror("Error","Invalid Name: Name can't consist 1 alphabet")
				cal_win_nm_ent.delete(0,END)
				cal_win_nm_ent.focus()
				return
			a = cal_win_age_ent.get()
			if not a.isdigit():
				showerror("Error","Invalid Age: Enter Numbers")
				cal_win_age_ent.delete(0,END)
				cal_win_age_ent.focus()
				return
			elif (int(a) <= 2):
				showerror("Error", "Invalid Age: Age should be greater than 2")
				cal_win_age_ent.delete(0,END)
				cal_win_age_ent.focus()
				return
			p = cal_win_phone_ent.get()
			if not p.isdigit():
				showerror("Error","Invalid Phone Number: Enter Numbers")
				cal_win_phone_ent.delete(0,END)
				cal_win_phone_ent.focus()
				return
			elif len(str(p))!=10:
				showerror("Error","Invalid Phone Number: Number should have length of 10")
				cal_win_phone_ent.delete(0,END)
				cal_win_phone_ent.focus()
				return
			gen = ch.get()
			if gen == 1:
				g = "male"
			elif gen == 2:
				g = "female"				
			h = float(cal_win_ht_ent.get())
			if type(h)!=float:
				showerror("Error","Invalid Height: Enter Numbers")
				cal_win_ht_ent.delete(0,END)
				cal_win_ht_ent.focus()	
				return
			w = float(cal_win_wg_ent.get())
			if type(w)!=float	:
				print("True")
				showerror("Error","Invalid Weight: Enter Numbers")
				cal_win_wg_ent.delete(0,END)
				cal_win_wg_ent.focus()
				return
			he = float(h)
			we = float(w)
			b = we / (he**2)
			msg = ""
			if b<18.5:
				msg= "Underweight!"
			elif 25>b>=18.5:
				msg = "Normal Weight!"
			elif 29.9>b>25.0:
				msg = "Pre Obesity"
			else:
				msg = "Obese!"
			bmi = round(b,2)
			print(bmi)
			cursor.execute(sql % (n,int(a),int(p),g,bmi))
			con.commit()
			cal_win_nm_ent.delete(0,END)
			cal_win_age_ent.delete(0,END)
			cal_win_phone_ent.delete(0,END)
			cal_win_genm.deselect()
			cal_win_genf.deselect()
			cal_win_ht_ent.delete(0,END)
			cal_win_wg_ent.delete(0,END)
			cal_win_nm_ent.focus()
			showinfo(title="Success", message="BMI="+str(bmi)+"\nYou are "+msg)
		except Exception as e:
			print("issue",e)
		finally:
			if con is not None:
				con.close()
				print("Disconnected!")
		
#calculate
	cal_win = Toplevel(menu)
	cal_win.title("Calculate")
	cal_win.geometry("800x500+0+0")
	cal_win.configure(background = '#ADD8E6')
	ch = IntVar()
	cal_win_nm = Label(cal_win,text = "Enter Name: ",font = font1)
	cal_win_age = Label(cal_win,text = "Enter Age: ",font = font1)
	cal_win_phone = Label(cal_win,text = "Enter Phone: ",font = font1)
	cal_win_gen = Label(cal_win,text = "Gender: ",font = font1)
	cal_win_ht = Label(cal_win,text = "Enter height in mtr: ",font = font1)
	cal_win_wg = Label(cal_win,text = "Enter weight in kg: ",font = font1)
	cal_win_calb = Button(cal_win, text = "Calculate", font = font1, command = calculate)
	cal_win_back = Button(cal_win,text = "Back", font = font1, command = c3)
	cal_win_convb = Button(cal_win,text = "Convert", font = font1, command = c2)
	cal_win_nm.place(x=10, y=10)
	cal_win_age.place(x=10, y=60)
	cal_win_phone.place(x=10, y=110)
	cal_win_gen.place(x=10, y=160)
	cal_win_ht.place(x=10, y=230)
	cal_win_wg.place(x=10, y=290)
	cal_win_nm_ent= Entry(cal_win, bd = 2 , font=font2)
	cal_win_age_ent= Entry(cal_win, bd = 2 , font=font2)
	cal_win_phone_ent= Entry(cal_win, bd = 2 , font=font2)
	cal_win_ht_ent= Entry(cal_win, bd = 2 , font=font2)
	cal_win_wg_ent= Entry(cal_win, bd = 2 , font=font2)
	cal_win_nm_ent.place(x=300, y=10)
	cal_win_age_ent.place(x=300, y=60)
	cal_win_phone_ent.place(x=300, y=110)
	cal_win_ht_ent.place(x=300, y=230)
	cal_win_wg_ent.place(x=300, y=290)
	cal_win_calb.place(x = 30, y = 380)
	cal_win_back.place(x = 200, y = 380)
	cal_win_convb.place(x = 650 ,y = 230)
	cal_win_genm = Radiobutton(cal_win,text = "Male",variable = ch, value=1,font = font1)
	cal_win_genf = Radiobutton(cal_win,text = "Female",variable = ch, value=2,font = font1)
	cal_win_genm.place(x=300, y=160)
	cal_win_genf.place(x=500, y=160)
	cal_win.withdraw()
	def c4():
		cal_win.deiconify()
		con_win.withdraw()
		cal_win_ht_ent.delete(0,END)
		f = con_win_fe.get()
		i = con_win_ie.get()
		me = (float(f)*0.3048)+(float(i)*0.0254)
		con_win_fe.delete(0,END)
		con_win_ie.delete(0,END)
		cal_win_ht_ent.insert(0,me)
	#height convert
	con_win = Toplevel(cal_win)
	con_win.title("Height Converter")
	con_win.geometry("800x500+0+0")
	con_win.configure(background = '#90EE90')
	con_win_la = Label(con_win,text = "Enter your height", font = font1)  
	con_win_fl = Label(con_win,text = "Feet",font = font1)
	con_win_il = Label(con_win,text = "Inches",font = font1)
	con_win_fe = Entry(con_win,bd = 6, font = font2)
	con_win_ie = Entry(con_win,bd = 6, font = font2)
	con_win_conb = Button(con_win, text = "Convert",font = font1,command = c4)
	con_win_la.pack(pady = 15)
	con_win_fl.pack(pady = 20)
	con_win_fe.pack(pady = 15)
	con_win_il.pack(pady = 20)	
	con_win_ie.pack(pady = 15)
	con_win_conb.pack(pady = 15)
	con_win.withdraw()

#history
	recs=""
	def bc():
		menu.deiconify()
		his_win.withdraw()
	def refresh():
		db = mysql.connector.connect(host = "localhost",user = "root",password = "abc456",database = "bmi")
		cursor = db.cursor()
		cursor.execute("select * from rec order by id desc limit 3")
		recs = cursor.fetchall()
		his_win_rec.config(text = "Name:"+str(recs[0][1])+"| Age:"+str(recs[0][2])+"| Phone No.:"+str(recs[0][3])+"| Gender:"+str(recs[0][4])+"| BMI:"+str(recs[0][5])+"\n\n"+"Name:"+str(recs[1][1])+"| Age:"+str(recs[1][2])+"| Phone No.:"+str(recs[1][3])+"| Gender:"+str(recs[1][4])+"| BMI:"+str(recs[1][5])+"\n\n"+"Name:"+str(recs[2][1])+"| Age:"+str(recs[2][2])+"| Phone No.:"+str(recs[2][3])+"| Gender:"+str(recs[2][4])+"| BMI:"+str(recs[2][5]),font = font2)
		his_win_rec.pack(pady = 10)
		
	his_win = Toplevel(menu)
	his_win.title("History")
	his_win.geometry("1000x600+0+0")
	his_win.configure(background = '#FFFF00')
	fonthis = ("Arial",40,"bold")
	his_win_ex = Label(his_win,text = "Previous Records",font = fonthis)
	his_win_ex.pack(pady = 10)
	his_win_ref = Button(his_win,text = "Refresh",bd = 2,font = font1,command = refresh)
	his_win_ref.pack(pady = 20)
	his_win_rec = Label(his_win,text = "Press Refresh",font = font2)
	his_win_rec.pack(pady = 10)
	his_win_back = Button(his_win,text = "Back",bd = 2,font = font1,command = bc)
	his_win_back.pack(pady = 70)
	his_win.withdraw()
splash.after(3000,menu) 
mainloop()