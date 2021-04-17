import discord,json,asyncio,time,traceback,sys,os,base64,gd,io,datetime,secrets,logging
from discord.utils import *
from itertools import chain
from urllib.request import urlopen
import mysql.connector as MC
from mysql.connector import errorcode
from urllib.parse import unquote
from re import search
from PIL import Image,ImageFont,ImageDraw

#########################

# Configs for database :

dbhost = "localhost"
dbdatabase = "database"
dbuser = "user"
dbpassword = "password"

#########################

# Configs in globally :

linkwebsite = "clarifygdps.com"
language_default = "en"
pic_ext = ['.jpg','.png','.jpeg']
color_palette = ['0x7dff00','0x00ff01','0x00ff7e','0x01ffff','0x01c8ff','0x0000ff','0x0000ff','0x7d00ff','0xba00ff','0xff01ff','0xff007d','0xff007d','0xff0100','0xfe4b00','0xff7e01','0xffb900','0xffff02','0xffffff','0xafafaf','0x5a5a5a','0x000000','0x7d7d00','0x649600','0x4caf01','0x019600','0x00b04b','0x009563','0x007d7e','0x006496','0x004baf','0x000197','0x4b00af','0x630095','0x7d007c','0x960064','0xaf004b','0x970001','0x973200','0xaf4c00','0x966401','0xff7d7e','0x7cffb0','0x7d7dff','0xfeff7d','0x7fffff','0xff7dff']

jouca = 216708683290247168

TOKEN = "TOKEN"
prefix = "req!"

#########################

left = u"\u2B05"
right = u"\u27A1"

#########################

# When loading the bot :

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

gdclient = gd.Client()
client = discord.Client(
	status="online",
	shard_count=3,
	chunk_guilds_at_startup=False,
	heartbeat_timeout=60)

try:
	conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
	cursor = conn.cursor()
except MC.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is not right with your username or your password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
finally:
	if(conn.is_connected()):
		cursor.close()
		conn.close()
		print("Connection Established !")

conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
cursor = conn.cursor(buffered=True)

#########################

@client.event
async def on_message(message):
	try:
		def levelfinder(levelid,var):
			serveur = var
			data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={levelid}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
			result = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
			if result == "-1":
				cursor.execute(f"DELETE FROM levels WHERE levelid = %s", (levelid, ))
				conn.commit()
				levelname = "~~Level Deleted~~"
				creator = "__Restart the command req!queue__"
				downloads = "0"
				likes = "0"
				rating = "0"
				stars = "0"
				featured = "0"
				epic = "0"
				demon = "0"
				demondifficulty = "0"
				objectplus = "0"
				isAuto = "0"
			elif result != "-1":
				result = result.split(":")
				levelname = result[3]
				creator = convertinfo("u","n",result[7])
				downloads = result[13]
				likes = result[19]
				rating = result[11]
				stars = result[27]
				featured = result[29]
				epic = result[31]
				demon = result[21]
				demondifficulty = result[23]
				objectplus = result[33]
				isAuto = result[25]
			ratingemote = None
			if int(likes) >= 0:
				likesemote = "<:like:472908805131337737>"
			elif int(likes) < 0:
				likesemote = "<:dislike:472907672744624128>"
			if demon is not "1":
				if int(stars) == 0:
					if int(rating) == 0:
						ratingemote = "<:icon_na:472908488406859776>"
					elif int(rating) == 10:
						ratingemote = "<:icon_easy:472908189059383296>"
					elif int(rating) == 20:
						ratingemote = "<:icon_normal:472908581319213056>"
					elif int(rating) == 30:
						ratingemote = "<:icon_hard:472908253408395296>"
					elif int(rating) == 40:
						ratingemote = "<:icon_harder:472908316301852683>"
					elif int(rating) == 50:
						ratingemote = "<:icon_insane:472908421209784320>"

				if int(rating) == 0:
					if int(featured) == 0:
						ratingemote = "<:icon_na:472908488406859776>"
					elif int(featured) > 0:
						ratingemote = "<:icon_na_featured:472908513677541416>"
					if int(epic) == 1:
						ratingemote = "<:icon_na_epic:472908540726476850>"
				elif int(rating) == 10:
					if int(featured) == 0:
						ratingemote = "<:icon_easy:472908189059383296>"
					elif int(featured) > 0:
						ratingemote = "<:icon_easy_featured:472908214766141471>"
					if int(epic) == 1:
						ratingemote = "<:icon_easy_epic:472908231803666432>"
				elif int(rating) == 20:
					if int(featured) == 0:
						ratingemote = "<:icon_normal:472908581319213056>"
					elif int(featured) > 0:
						ratingemote = "<:icon_normal_featured:472908602613563392>"
					if int(epic) == 1:
						ratingemote = "<:icon_normal_epic:472908627158761473>"
				elif int(rating) == 30:
					if int(featured) == 0:
						ratingemote = "<:icon_hard:472908253408395296>"
					elif int(featured) > 0:
						ratingemote = "<:icon_hard_featured:472908272781754369>"
					if int(epic) == 1:
						ratingemote = "<:icon_hard_epic:472908293837160459>"
				elif int(rating) == 40:
					if int(featured) == 0:
						ratingemote = "<:icon_harder:472908316301852683>"
					elif int(featured) > 0:
						ratingemote = "<:icon_harder_featured:472908356928143370>"
					if int(epic) == 1:
						ratingemote = "<:icon_harder_epic:472908377991675914>"
				elif int(rating) == 50:
					if int(featured) == 0:
						ratingemote = "<:icon_insane:472908421209784320>"
					elif int(featured) > 0:
						ratingemote = "<:icon_insane_featured:472908439958323211>"
					if int(epic) == 1:
						ratingemote = "<:icon_insane_epic:472908465761812490>"
				try:
					if int(isAuto) == 1:
						if int(featured) == 0:
							ratingemote = "<:icon_auto:472907799987486768>"
						elif int(featured) > 0:
							ratingemote = "<:icon_auto_featured:472907828185792532>"
						if int(epic) == 1:
							ratingemote = "<:icon_auto_epic:472907845915115541>"
				except ValueError:
					pass
			elif int(demon) == 1:
				if int(stars) == 0:
					if int(demondifficulty) == 3:
						ratingemote = "<:icon_demon_easy:472907861102559262>"
					elif int(demondifficulty) == 4:
						ratingemote = "<:icon_demon_medium:472908111053586433>"
					elif int(demondifficulty) == 0:
						ratingemote = "<:icon_demon_hard:472907978094411776>"
					elif int(demondifficulty) == 5:
						ratingemote = "<:icon_demon_insane:472908041960947712>"
					elif int(demondifficulty) == 6:
						ratingemote = "<:icon_demon_extreme:472907914110304267>"
				if int(demondifficulty) == 3:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_easy:472907861102559262>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_easy_featured:472907878790070273>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_easy_epic:472907895114301440>"
				elif int(demondifficulty) == 4:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_medium:472908111053586433>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_medium_featured:472908128472793089>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_medium_epic:472908148978745344>"
				elif int(demondifficulty) == 0:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_hard:472907978094411776>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_hard_featured:472907996901408778>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_hard_epic:472908016149069835>"
				elif int(demondifficulty) == 5:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_insane:472908041960947712>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_insane_featured:472908062269636640>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_insane_epic:472908084407173120>"
				elif int(demondifficulty) == 6:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_extreme:472907914110304267>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_extreme_featured:472907934633033738>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_extreme_epic:472907957978398720>"
			connect = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
			cursor2 = connect.cursor(buffered=True)
			query12 = f"SELECT * FROM setup WHERE serverid = {var}"
			cursor2.execute(query12)
			result123 = cursor2.fetchone()
			removerated = result123[12]
			if removerated == "1" and stars != "0":
				cursor.execute(f"DELETE FROM levels WHERE levelid = %s", (levelid, ))
				conn.commit()
				levelname = "~~RemoveRated Bot~~"
				creator = "__Restart the command req!queue__"
				rating = "0"
				stars = "0"
				featured = "0"
				epic = "0"
				demon = "0"
				demondifficulty = "0"
				objectplus = "0"
				isAuto = "0"
			return stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote

		def levelfinder2(levelid,var):
			data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={levelid}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
			result = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
			if result == "-1":
				cursor.execute(f"DELETE FROM levels WHERE levelid = %s", (levelid, ))
				conn.commit()
				levelname = "~~Level Deleted~~"
				creator = "__Restart the command req!queue__"
				downloads = "0"
				likes = "0"
				rating = "0"
				stars = "0"
				featured = "0"
				epic = "0"
				demon = "0"
				demondifficulty = "0"
				objectplus = "0"
				isAuto = "0"
			elif result != "-1":
				result = result.split(":")
				levelname = result[3]
				creator = convertinfo("u","n",result[7])
				downloads = result[13]
				likes = result[19]
				rating = result[11]
				stars = result[27]
				featured = result[29]
				epic = result[31]
				demon = result[21]
				demondifficulty = result[23]
				objectplus = result[33]
				isAuto = result[25]
			ratingemote = None
			if int(likes) >= 0:
				likesemote = "<:like:472908805131337737>"
			elif int(likes) < 0:
				likesemote = "<:dislike:472907672744624128>"
			if demon is not "1":
				if int(stars) == 0:
					if int(rating) == 0:
						ratingemote = "<:icon_na:472908488406859776>"
					elif int(rating) == 10:
						ratingemote = "<:icon_easy:472908189059383296>"
					elif int(rating) == 20:
						ratingemote = "<:icon_normal:472908581319213056>"
					elif int(rating) == 30:
						ratingemote = "<:icon_hard:472908253408395296>"
					elif int(rating) == 40:
						ratingemote = "<:icon_harder:472908316301852683>"
					elif int(rating) == 50:
						ratingemote = "<:icon_insane:472908421209784320>"

				if int(rating) == 0:
					if int(featured) == 0:
						ratingemote = "<:icon_na:472908488406859776>"
					elif int(featured) > 0:
						ratingemote = "<:icon_na_featured:472908513677541416>"
					if int(epic) == 1:
						ratingemote = "<:icon_na_epic:472908540726476850>"
				elif int(rating) == 10:
					if int(featured) == 0:
						ratingemote = "<:icon_easy:472908189059383296>"
					elif int(featured) > 0:
						ratingemote = "<:icon_easy_featured:472908214766141471>"
					if int(epic) == 1:
						ratingemote = "<:icon_easy_epic:472908231803666432>"
				elif int(rating) == 20:
					if int(featured) == 0:
						ratingemote = "<:icon_normal:472908581319213056>"
					elif int(featured) > 0:
						ratingemote = "<:icon_normal_featured:472908602613563392>"
					if int(epic) == 1:
						ratingemote = "<:icon_normal_epic:472908627158761473>"
				elif int(rating) == 30:
					if int(featured) == 0:
						ratingemote = "<:icon_hard:472908253408395296>"
					elif int(featured) > 0:
						ratingemote = "<:icon_hard_featured:472908272781754369>"
					if int(epic) == 1:
						ratingemote = "<:icon_hard_epic:472908293837160459>"
				elif int(rating) == 40:
					if int(featured) == 0:
						ratingemote = "<:icon_harder:472908316301852683>"
					elif int(featured) > 0:
						ratingemote = "<:icon_harder_featured:472908356928143370>"
					if int(epic) == 1:
						ratingemote = "<:icon_harder_epic:472908377991675914>"
				elif int(rating) == 50:
					if int(featured) == 0:
						ratingemote = "<:icon_insane:472908421209784320>"
					elif int(featured) > 0:
						ratingemote = "<:icon_insane_featured:472908439958323211>"
					if int(epic) == 1:
						ratingemote = "<:icon_insane_epic:472908465761812490>"
				try:
					if int(isAuto) == 1:
						if int(featured) == 0:
							ratingemote = "<:icon_auto:472907799987486768>"
						elif int(featured) > 0:
							ratingemote = "<:icon_auto_featured:472907828185792532>"
						if int(epic) == 1:
							ratingemote = "<:icon_auto_epic:472907845915115541>"
				except ValueError:
					pass
			elif int(demon) == 1:
				if int(stars) == 0:
					if int(demondifficulty) == 3:
						ratingemote = "<:icon_demon_easy:472907861102559262>"
					elif int(demondifficulty) == 4:
						ratingemote = "<:icon_demon_medium:472908111053586433>"
					elif int(demondifficulty) == 0:
						ratingemote = "<:icon_demon_hard:472907978094411776>"
					elif int(demondifficulty) == 5:
						ratingemote = "<:icon_demon_insane:472908041960947712>"
					elif int(demondifficulty) == 6:
						ratingemote = "<:icon_demon_extreme:472907914110304267>"
				if int(demondifficulty) == 3:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_easy:472907861102559262>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_easy_featured:472907878790070273>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_easy_epic:472907895114301440>"
				elif int(demondifficulty) == 4:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_medium:472908111053586433>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_medium_featured:472908128472793089>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_medium_epic:472908148978745344>"
				elif int(demondifficulty) == 0:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_hard:472907978094411776>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_hard_featured:472907996901408778>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_hard_epic:472908016149069835>"
				elif int(demondifficulty) == 5:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_insane:472908041960947712>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_insane_featured:472908062269636640>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_insane_epic:472908084407173120>"
				elif int(demondifficulty) == 6:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_extreme:472907914110304267>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_extreme_featured:472907934633033738>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_extreme_epic:472907957978398720>"
			return stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote

		def reqsearch(level):
			data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={level}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
			result = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
			result = result.split(":")
			idlevel = result[1]
			version = result[5]
			gdversion2 = result[17]
			levelname = result[3]
			creator = convertinfo("u","n",result[7])
			description = result[35]
			downloads = result[13]
			likes = result[19]
			rating = result[11]
			stars = result[27]
			coins = result[43]
			verifiedcoins = result[45]
			length = result[37]
			isAuto = result[25]
			featured = result[29]
			epic = result[31]
			demon = result[21]
			demondifficulty = result[23]
			objectplus = result[33]
			ratingemote = None

			if int(gdversion2) == 1:
				gdversion = "1.0"
			elif int(gdversion2) == 2:
				gdversion = "1.1"
			elif int(gdversion2) == 3:
				gdversion = "1.2"
			elif int(gdversion2) == 4:
				gdversion = "1.3"
			elif int(gdversion2) == 5:
				gdversion = "1.4"
			elif int(gdversion2) == 6:
				gdversion = "1.5"
			elif int(gdversion2) == 7:
				gdversion = "1.6"
			elif int(gdversion2) == 10:
				gdversion = "1.7"
			elif int(gdversion2) == 18:
				gdversion = "1.8"
			elif int(gdversion2) == 19:
				gdversion = "1.9"
			elif int(gdversion2) == 20:
				gdversion = "2.0"
			elif int(gdversion2) == 21:
				gdversion = "2.1"

			if int(length) == 0:
				lengthvalue = "TINY"
			elif int(length) == 1:
				lengthvalue = "SHORT"
			elif int(length) == 2:
				lengthvalue = "MEDIUM"
			elif int(length) == 3:
				lengthvalue = "LONG"
			elif int(length) == 4:
				lengthvalue = "XL"

			if int(likes) >= 0:
				likesemote = "<:like:472908805131337737>"
			elif int(likes) < 0:
				likesemote = "<:dislike:472907672744624128>"
			if demon is not "1":
				if int(stars) == 0:
					if int(rating) == 0:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/T3YfK5d.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/C4oMYGU.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/hDBDGzX.png"
						color = 0x909090
					elif int(rating) == 10:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/kWHZa5d.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/5p9eTaR.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/k2lJftM.png"
						color = 0x019efd
					elif int(rating) == 20:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/zURUazz.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/Q1MYgu4.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/VyV8II6.png"
						color = 0x2bf90b
					elif int(rating) == 30:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/YV4Afz2.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/8DeaxfL.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/SqnA9kJ.png"
						color = 0xebf90b
					elif int(rating) == 40:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/5lT74Xj.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/n5kA2Tv.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/Y7bgUu9.png"
						color = 0xf92f0b
					elif int(rating) == 50:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/PeOvWuq.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/t8JmuIw.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/GdS2f8f.png"
						color = 0xf90b9b
					try:
						if int(isAuto) == 1:
							if int(featured) == 0:
								ratingemote = "https://i.imgur.com/7xI8EOp.png"
							elif int(featured) > 0:
								ratingemote = "https://i.imgur.com/eMwuWmx.png"
							if int(epic) == 1:
								ratingemote = "https://i.imgur.com/QuRBnpB.png"
							color = 0xf9b30b
					except ValueError:
						pass
				elif int(stars) != 0:
					if int(rating) == 10:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/yG1U6RP.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/Kyjevk1.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/wl575nH.png"
						color = 0x019efd
					elif int(rating) == 20:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/cx8tv98.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/1v3p1A8.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/S3PhlDs.png"
						color = 0x2bf90b
					elif int(rating) == 30:
						if int(stars) == 4:
							if int(featured) == 0:
								ratingemote = "https://i.imgur.com/XnUynAa.png"
							elif int(featured) > 0:
								ratingemote = "https://i.imgur.com/VW4yufj.png"
							if int(epic) == 1:
								ratingemote = "https://i.imgur.com/toyo1Cd.png"
						elif int(stars) == 5:
							if int(featured) == 0:
								ratingemote = "https://i.imgur.com/Odx0nAT.png"
							elif int(featured) > 0:
								ratingemote = "https://i.imgur.com/HiyX5DD.png"
							if int(epic) == 1:
								ratingemote = "https://i.imgur.com/W11eyJ9.png"
						color = 0xebf90b
					elif int(rating) == 40:
						if int(stars) == 6:
							if int(featured) == 0:
								ratingemote = "https://i.imgur.com/e499HCB.png"
							elif int(featured) > 0:
								ratingemote = "https://i.imgur.com/b7J4AXi.png"
							if int(epic) == 1:
								ratingemote = "https://i.imgur.com/9x1ddvD.png"
						elif int(stars) == 7:
							if int(featured) == 0:
								ratingemote = "https://i.imgur.com/dJoUDUk.png"
							elif int(featured) > 0:
								ratingemote = "https://i.imgur.com/v50cZBZ.png"
							if int(epic) == 1:
								ratingemote = "https://i.imgur.com/X3N5sm1.png"
						color = 0xf92f0b
					elif int(rating) == 50:
						if int(stars) == 8:
							if int(featured) == 0:
								ratingemote = "https://i.imgur.com/RDVJDaO.png"
							elif int(featured) > 0:
								ratingemote = "https://i.imgur.com/PYJ5T0x.png"
							if int(epic) == 1:
								ratingemote = "https://i.imgur.com/N2pjW2W.png"
						elif int(stars) == 9:
							if int(featured) == 0:
								ratingemote = "https://i.imgur.com/5VA2qDb.png"
							elif int(featured) > 0:
								ratingemote = "https://i.imgur.com/byhPbgR.png"
							if int(epic) == 1:
								ratingemote = "https://i.imgur.com/qmfey5L.png"
						color = 0xf90b9b
					try:
						if int(isAuto) == 1:
							if int(featured) == 0:
								ratingemote = "https://i.imgur.com/Fws2s3b.png"
							elif int(featured) > 0:
								ratingemote = "https://i.imgur.com/DplWGja.png"
							if int(epic) == 1:
								ratingemote = "https://i.imgur.com/uzYx91v.png"
							color = 0xf9b30b
					except ValueError:
						pass
			elif int(demon) == 1:
				if int(stars) == 0:
					if int(demondifficulty) == 3:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/45GaxRN.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/r2WNVw0.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/idesUcS.png"
						color = 0x0b27f9
					elif int(demondifficulty) == 4:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/H3Swqhy.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/IaeyGY4.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/eEEzM6I.png"
						color = 0xdf0bf9
					elif int(demondifficulty) == 0:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/WhrTo7w.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/lVdup3A.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/xLFubIn.png"
						color = 0xff5757
					elif int(demondifficulty) == 5:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/fNC1iFH.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/1MpbSRR.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/ArGfdeh.png"
						color = 0xff0101
					elif int(demondifficulty) == 6:
						if int(featured) == 0:
							ratingemote = "https://i.imgur.com/v74cX5I.png"
						elif int(featured) > 0:
							ratingemote = "https://i.imgur.com/4MMF8uE.png"
						if int(epic) == 1:
							ratingemote = "https://i.imgur.com/p250YUh.png"
						color = 0xbf0000
				if int(demondifficulty) == 3:
					if int(featured) == 0:
						ratingemote = "https://i.imgur.com/0zM0VuT.png"
					elif int(featured) > 0:
						ratingemote = "https://i.imgur.com/fFq5lbN.png"
					if int(epic) == 1:
						ratingemote = "https://i.imgur.com/wUGOGJ7.png"
					color = 0x0b27f9
				elif int(demondifficulty) == 4:
					if int(featured) == 0:
						ratingemote = "https://i.imgur.com/lvpPepA.png"
					elif int(featured) > 0:
						ratingemote = "https://i.imgur.com/kkAZv5O.png"
					if int(epic) == 1:
						ratingemote = "https://i.imgur.com/ghco42q.png"
					color = 0xdf0bf9
				elif int(demondifficulty) == 0:
					if int(featured) == 0:
						ratingemote = "https://i.imgur.com/jLBD7cO.png"
					elif int(featured) > 0:
						ratingemote = "https://i.imgur.com/7deDmTQ.png"
					if int(epic) == 1:
						ratingemote = "https://i.imgur.com/xtrTl4r.png"
					color = 0xff5757
				elif int(demondifficulty) == 5:
					if int(featured) == 0:
						ratingemote = "https://i.imgur.com/nLZqoyQ.png"
					elif int(featured) > 0:
						ratingemote = "https://i.imgur.com/RWqIpYL.png"
					if int(epic) == 1:
						ratingemote = "https://i.imgur.com/2BWY8pO.png"
					color = 0xff0101
				elif int(demondifficulty) == 6:
					if int(featured) == 0:
						ratingemote = "https://i.imgur.com/DEr1HoM.png"
					elif int(featured) > 0:
						ratingemote = "https://i.imgur.com/xat5en2.png"
					if int(epic) == 1:
						ratingemote = "https://i.imgur.com/gFndlkZ.png"
					color = 0xbf0000

			return stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color

		def reqsearch2(level):
			data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={level}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
			result = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
			result3 = result.split(":")
			idlevel = result3[1]
			songidpart = result3[53]
			result4 = songidpart.split("#")
			customsongid = result4[0]
			result5 = result.split("#")
			result5 = result5[2]
			result2 = result5.split("~|~")

			try:
				songname = result2[3]
				songauthor = result2[7]
				songid = result2[1]
				sizesong = result2[9]
				songlink = result2[13]
			except IndexError:
				officialsong = result3[15]
				if int(officialsong) == 0 and int(customsongid) == 0 :
					songname = "Stereo Madness"
					songauthor = "ForeverBound"
					songid = 500476
					sizesong = "7.6"
					songlink = "https://youtu.be/JhKyKEDxo8Q"
				elif int(officialsong) == 1:
					songname = "Back on Track"
					songauthor = "DJVI"
					songid = 522654
					sizesong = "6.9"
					songlink = "https://youtu.be/N9vDTYZpqXM"
				elif int(officialsong) == 2:
					songname = "Polargeist"
					songauthor = "Step"
					songid = 523561
					sizesong = "4.3"
					songlink = "https://youtu.be/HkFbziBbvy8"
				elif int(officialsong) == 3:
					songname = "Dry Out"
					songauthor = "DJVI"
					songid = 498543
					sizesong = "6.2"
					songlink = "https://youtu.be/FnXabH2q2A0"
				elif int(officialsong) == 4:
					songname = "Base After Base"
					songauthor = "DJVI"
					songid = 404997
					sizesong = "5.9"
					songlink = "https://youtu.be/TZULkgQPHt0"
				elif int(officialsong) == 5:
					songname = "Can't Let Go"
					songauthor = "DJVI"
					songid = 485351
					sizesong = "7.1"
					songlink = "https://youtu.be/fLnF-QnR1Zw"
				elif int(officialsong) == 6:
					songname = "Jumper"
					songauthor = "Waterflame"
					songid = 168734
					sizesong = "3"
					songlink = "https://youtu.be/ZXHO4AN_49Q"
				elif int(officialsong) == 7:
					songname = "Time Machine"
					songauthor = "Waterflame"
					songid = 291458
					sizesong = "6.3"
					songlink = "https://youtu.be/zZ1L9JD6l0g"
				elif int(officialsong) == 8:
					songname = "Cycles"
					songauthor = "DJVI"
					songid = 529148
					sizesong = "7.1"
					songlink = "https://youtu.be/KDdvGZn6Gfs"
				elif int(officialsong) == 9:
					songname = "xStep"
					songauthor = "DJVI"
					songid = 516735
					sizesong = "7.3"
					songlink = "https://youtu.be/PSvYfVGyQfw"
				elif int(officialsong) == 10:
					songname = "Clutterfunk"
					songauthor = "Waterflame"
					songid = 505816
					sizesong = "9.7"
					songlink = "https://youtu.be/D5uJOpItgNg"
				elif int(officialsong) == 11:
					songname = "Theory Of Everything"
					songauthor = "DJ-Nate"
					songid = 350290
					sizesong = "6"
					songlink = "https://youtu.be/ZUGJ0vWqfis"
				elif int(officialsong) == 12:
					songname = "Electroman Adventures"
					songauthor = "Waterflame"
					songid = 479319
					sizesong = "5.8"
					songlink = "https://youtu.be/Pb6KyewC_Vg"
				elif int(officialsong) == 13:
					songname = "Clubstep"
					songauthor = "DJ-Nate"
					songid = 396093
					sizesong = "6.3"
					songlink = "https://youtu.be/T7Wff9xaqjc"
				elif int(officialsong) == 14:
					songname = "Electrodynamix"
					songauthor = "DJ-Nate"
					songid = 368392
					sizesong = "7.8"
					songlink = "https://youtu.be/HeQGcCtk4bc"
				elif int(officialsong) == 15:
					songname = "Hexagon Force"
					songauthor = "Waterflame"
					songid = 568699
					sizesong = "9.7"
					songlink = "https://youtu.be/afwK743PL2Y"
				elif int(officialsong) == 16:
					songname = "Blast Processing"
					songauthor = "Waterflame"
					songid = 507560
					sizesong = "10.7"
					songlink = "https://youtu.be/Z5RufkDHsdM"
				elif int(officialsong) == 17:
					songname = "Theory Of Everything 2"
					songauthor = "DJ-Nate"
					songid = 472925
					sizesong = "3.9"
					songlink = "https://youtu.be/fn98711CEoI"
				elif int(officialsong) == 18:
					songname = "Geometrical Dominator"
					songauthor = "Waterflame"
					songid = 641172
					sizesong = "4"
					songlink = "https://youtu.be/8so76wQOioo"
				elif int(officialsong) == 19:
					songname = "Deadlocked"
					songauthor = "F-777"
					songid = 503731
					sizesong = "7.9"
					songlink = "https://youtu.be/OPBECnDBiRQ"
				elif int(officialsong) == 20:
					songname = "Fingerdash"
					songauthor = "MDK"
					songid = 860287
					sizesong = "2"
					songlink = "https://youtu.be/BuPmq7yjDnI"
				return songname,songauthor,songid,sizesong,songlink,officialsong
			return songname,songauthor,songid,sizesong,songlink

		def reqsearch3(songid):
			result = urlopen(f"http://www.boomlings.com/database/testSong.php?songID={songid}").read().decode()
			result = result.split("</br>")
			songartist = result[0]
			artistwhitelisted = result[1]
			artistscouted = result[2]
			return songartist,artistscouted,artistwhitelisted

		def reqsearchfirst(level):
			data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={level}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
			result2 = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
			return result2

		def queuedecryptor(levels):
			levels = ",".join(levels)
			string = f"gameVersion=21&binaryVersion=35&gdw=0&type=10&str={levels}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
			levels = urlopen(f"http://www.boomlings.com/database/getGJLevels21.php",string).read().decode()
			return levels

		def queueinfo(level):
			result = level.split(":")
			levelid = result[1]
			levelname = result[3]
			downloads = result[13]
			likes = result[19]
			rating = result[11]
			stars = result[27]
			featured = result[29]
			epic = result[31]
			demon = result[21]
			demondifficulty = result[23]
			objectplus = result[33]
			isAuto = result[25]
			ratingemote = None
			if int(likes) >= 0:
				likesemote = "<:like:472908805131337737>"
			elif int(likes) < 0:
				likesemote = "<:dislike:472907672744624128>"
			if demon is not "1":
				if int(stars) == 0:
					if int(rating) == 0:
						ratingemote = "<:icon_na:472908488406859776>"
					elif int(rating) == 10:
						ratingemote = "<:icon_easy:472908189059383296>"
					elif int(rating) == 20:
						ratingemote = "<:icon_normal:472908581319213056>"
					elif int(rating) == 30:
						ratingemote = "<:icon_hard:472908253408395296>"
					elif int(rating) == 40:
						ratingemote = "<:icon_harder:472908316301852683>"
					elif int(rating) == 50:
						ratingemote = "<:icon_insane:472908421209784320>"

				if int(rating) == 0:
					if int(featured) == 0:
						ratingemote = "<:icon_na:472908488406859776>"
					elif int(featured) > 0:
						ratingemote = "<:icon_na_featured:472908513677541416>"
					if int(epic) == 1:
						ratingemote = "<:icon_na_epic:472908540726476850>"
				elif int(rating) == 10:
					if int(featured) == 0:
						ratingemote = "<:icon_easy:472908189059383296>"
					elif int(featured) > 0:
						ratingemote = "<:icon_easy_featured:472908214766141471>"
					if int(epic) == 1:
						ratingemote = "<:icon_easy_epic:472908231803666432>"
				elif int(rating) == 20:
					if int(featured) == 0:
						ratingemote = "<:icon_normal:472908581319213056>"
					elif int(featured) > 0:
						ratingemote = "<:icon_normal_featured:472908602613563392>"
					if int(epic) == 1:
						ratingemote = "<:icon_normal_epic:472908627158761473>"
				elif int(rating) == 30:
					if int(featured) == 0:
						ratingemote = "<:icon_hard:472908253408395296>"
					elif int(featured) > 0:
						ratingemote = "<:icon_hard_featured:472908272781754369>"
					if int(epic) == 1:
						ratingemote = "<:icon_hard_epic:472908293837160459>"
				elif int(rating) == 40:
					if int(featured) == 0:
						ratingemote = "<:icon_harder:472908316301852683>"
					elif int(featured) > 0:
						ratingemote = "<:icon_harder_featured:472908356928143370>"
					if int(epic) == 1:
						ratingemote = "<:icon_harder_epic:472908377991675914>"
				elif int(rating) == 50:
					if int(featured) == 0:
						ratingemote = "<:icon_insane:472908421209784320>"
					elif int(featured) > 0:
						ratingemote = "<:icon_insane_featured:472908439958323211>"
					if int(epic) == 1:
						ratingemote = "<:icon_insane_epic:472908465761812490>"
				try:
					if int(isAuto) == 1:
						if int(featured) == 0:
							ratingemote = "<:icon_auto:472907799987486768>"
						elif int(featured) > 0:
							ratingemote = "<:icon_auto_featured:472907828185792532>"
						if int(epic) == 1:
							ratingemote = "<:icon_auto_epic:472907845915115541>"
				except ValueError:
					pass
			elif int(demon) == 1:
				if int(stars) == 0:
					if int(demondifficulty) == 3:
						ratingemote = "<:icon_demon_easy:472907861102559262>"
					elif int(demondifficulty) == 4:
						ratingemote = "<:icon_demon_medium:472908111053586433>"
					elif int(demondifficulty) == 0:
						ratingemote = "<:icon_demon_hard:472907978094411776>"
					elif int(demondifficulty) == 5:
						ratingemote = "<:icon_demon_insane:472908041960947712>"
					elif int(demondifficulty) == 6:
						ratingemote = "<:icon_demon_extreme:472907914110304267>"
				if int(demondifficulty) == 3:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_easy:472907861102559262>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_easy_featured:472907878790070273>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_easy_epic:472907895114301440>"
				elif int(demondifficulty) == 4:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_medium:472908111053586433>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_medium_featured:472908128472793089>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_medium_epic:472908148978745344>"
				elif int(demondifficulty) == 0:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_hard:472907978094411776>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_hard_featured:472907996901408778>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_hard_epic:472908016149069835>"
				elif int(demondifficulty) == 5:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_insane:472908041960947712>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_insane_featured:472908062269636640>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_insane_epic:472908084407173120>"
				elif int(demondifficulty) == 6:
					if int(featured) == 0:
						ratingemote = "<:icon_demon_extreme:472907914110304267>"
					elif int(featured) > 0:
						ratingemote = "<:icon_demon_extreme_featured:472907934633033738>"
					if int(epic) == 1:
						ratingemote = "<:icon_demon_extreme_epic:472907957978398720>"
			query12 = f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1"
			cursor.execute(query12)
			result123 = cursor.fetchone()
			removerated = result123[12]
			if removerated == "1" and stars != "0":
				cursor.execute(f"DELETE FROM levels WHERE levelid = {levelid} LIMIT 1")
				conn.commit()
				levelname = f"~~{levelname}~~"
				rating = "0"
				downloads = "`This level have been rated and removed by RemoveRated.`"
				likes = "__Restart req!queue__"
				stars = "0"
				featured = "0"
				epic = "0"
				demon = "0"
				demondifficulty = "0"
				objectplus = "0"
				isAuto = "0"
			return stars,objectplus,levelname,ratingemote,stars,downloads,likes,likesemote
			
		def queueconstructor(embed,level,vid,number,levelid,pages,creatorplayer):
			stars,objectplus,levelname,ratingemote,stars,downloads,likes,likesemote = queueinfo(level)
			stars,objectplus,levelname,ratingemote,stars,downloads,likes,likesemote = str(stars),str(objectplus),str(levelname),str(ratingemote),str(stars),str(downloads),str(likes),str(likesemote)
			video = vid
			i = embed
			if int(stars) == 0:
				if int(objectplus) >= 40000:
					if video is not None:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} <:object_overflow:472908865953071115>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}", value=f"({video})", inline=False)
					else:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} <:object_overflow:472908865953071115>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}", value="\u200b", inline=False)
				elif int(objectplus) <= 39999:
					if video is not None:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote}\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}", value=f"({video})", inline=False)
					else:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote}\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}", value="\u200b", inline=False)
			elif int(stars) != 0:
				if int(objectplus) >= 40000:
					if video is not None:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} {stars}<:starrate:718204629858517003> <:object_overflow:472908865953071115>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}", value=f"({video})", inline=False)
					else:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} {stars}<:starrate:718204629858517003> <:object_overflow:472908865953071115>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}", value="\u200b", inline=False)
				elif int(objectplus) <= 39999:
					if video is not None:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} {stars}<:starrate:718204629858517003>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}", value=f"({video})", inline=False)
					else:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} {stars}<:starrate:718204629858517003>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}", value="\u200b", inline=False)				

		def myqueueconstructor(embed,level,vid,number,levelid,pages,server,creatorplayer):
			servername = client.get_guild(int(server))
			stars,objectplus,levelname,ratingemote,stars,downloads,likes,likesemote = queueinfo(level)
			stars,objectplus,levelname,ratingemote,stars,downloads,likes,likesemote = str(stars),str(objectplus),str(levelname),str(ratingemote),str(stars),str(downloads),str(likes),str(likesemote)
			video = vid
			i = embed
			if int(stars) == 0:
				if int(objectplus) >= 40000:
					if video is not None:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} <:object_overflow:472908865953071115>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}\n__{requestedserver} {servername}__", value=f"({video})", inline=False)
					else:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} <:object_overflow:472908865953071115>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}\n__{requestedserver} {servername}__", value="\u200b", inline=False)
				elif int(objectplus) <= 39999:
					if video is not None:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote}\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}\n__{requestedserver} {servername}__", value=f"({video})", inline=False)
					else:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote}\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}\n__{requestedserver} {servername}__", value="\u200b", inline=False)
			elif int(stars) != 0:
				if int(objectplus) >= 40000:
					if video is not None:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} {stars}<:starrate:718204629858517003> <:object_overflow:472908865953071115>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}\n__{requestedserver} {servername}__", value=f"({video})", inline=False)
					else:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} {stars}<:starrate:718204629858517003> <:object_overflow:472908865953071115>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}\n__{requestedserver} {servername}__", value="\u200b", inline=False)
				elif int(objectplus) <= 39999:
					if video is not None:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} {stars}<:starrate:718204629858517003>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}\n__{requestedserver} {servername}__", value=f"({video})", inline=False)
					else:
						pages[i].add_field(name=f"#{number} `{levelid}` {levelname} {by} {creatorplayer} {ratingemote} {stars}<:starrate:718204629858517003>\n<:downloads:472907713727430658> : {downloads}\n{likesemote} : {likes}\n__{requestedserver} {servername}__", value="\u200b", inline=False)

		def predicate(message, l, r):
			def check(reaction, user):
				if reaction.message.id != message.id or user == client.user:
					return False
				if l and reaction.emoji == left:
					return True
				if r and reaction.emoji == right:
					return True
				return False

			return check

		def convertinfo(type1,type2,value1):
			if type2=="n":
				r=1
			elif type2=="a":
				r=21
			elif type2=="u":
				r=3
			if type1=="n" or type1=="u":
				url = "http://www.boomlings.com/database/getGJUsers20.php"
				p = "str=%s&total=0&page=0&secret=Wmfd2893gb7"
			else:
				url = "http://www.boomlings.com/database/getGJUserInfo20.php"
				p = "accountID=0&gjp=&targetAccountID=%s&secret=Wmfd2893gb7"

			p = (p % (value1)).encode()
			data = urlopen(url,p).read().decode()
			if data == "-1":
				return "-1"

			return data.split(":")[r]

		def firstsync(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[0]
			achievementdesc = translate_messages[1]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url=f"http://clarifygdps.com/geometry-requests/emojies/linkage.png")
			return embed5

		def requestachievement1(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[3]
			achievementdesc = translate_messages[4]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/requests_0001.png")
			return embed5

		def requestachievement5(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[6]
			achievementdesc = translate_messages[7]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/requests_0005.png")
			return embed5

		def requestachievement10(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[9]
			achievementdesc = translate_messages[10]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/requests_0010.png")
			return embed5

		def requestachievement50(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[12]
			achievementdesc = translate_messages[13]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/requests_0050.png")
			return embed5

		def requestachievement100(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[15]
			achievementdesc = translate_messages[16]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/requests_0100.png")
			return embed5

		def reviewachievement1(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[18]
			achievementdesc = translate_messages[19]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/reviewed_0001.png")
			return embed5

		def reviewachievement5(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[21]
			achievementdesc = translate_messages[22]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/reviewed_0005.png")
			return embed5

		def reviewachievement10(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[24]
			achievementdesc = translate_messages[25]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/reviewed_0010.png")
			return embed5

		def reviewachievement50(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[27]
			achievementdesc = translate_messages[28]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/reviewed_0050.png")
			return embed5

		def reviewachievement100(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[30]
			achievementdesc = translate_messages[31]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/reviewed_0100.png")
			return embed5

		def reviewapprovedachievement1(user1):
			cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[33]
			achievementdesc = translate_messages[34]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/approved_0001.png")
			return embed5

		def reviewapprovedachievement5(user1):
			cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[36]
			achievementdesc = translate_messages[37]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/approved_0005.png")
			return embed5

		def reviewapprovedachievement10(user1):
			cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[39]
			achievementdesc = translate_messages[40]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/approved_0010.png")
			return embed5

		def reviewapprovedachievement50(user1):
			cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[42]
			achievementdesc = translate_messages[43]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/approved_0050.png")
			return embed5

		def reviewapprovedachievement100(user1):
			cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[45]
			achievementdesc = translate_messages[46]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/approved_0100.png")
			return embed5

		def reviewunapprovedachievement1(user1):
			cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[48]
			achievementdesc = translate_messages[49]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/unapproved_0001.png")
			return embed5

		def reviewunapprovedachievement5(user1):
			cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[51]
			achievementdesc = translate_messages[52]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/unapproved_0005.png")
			return embed5

		def reviewunapprovedachievement10(user1):
			cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[54]
			achievementdesc = translate_messages[55]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/unapproved_0010.png")
			return embed5

		def reviewunapprovedachievement50(user1):
			cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[57]
			achievementdesc = translate_messages[58]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/unapproved_0050.png")
			return embed5

		def reviewunapprovedachievement100(user1):
			cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[60]
			achievementdesc = translate_messages[61]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/unapproved_0100.png")
			return embed5

		def levelsentbygdmod(user1):
			cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[63]
			achievementdesc = translate_messages[64]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/modSend.png")
			return embed5

		def suggestidea(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[66]
			achievementdesc = translate_messages[67]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/suggestion.png")
			return embed5

		def approvedidea(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[69]
			achievementdesc = translate_messages[70]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/suggestionApproved.png")
			return embed5

		def approvedreport(author):
			cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
			try:
				language = cursor.fetchone()[0]
			except TypeError:
				language = language_default
			language2 = language
			translate_messages = open(f"language/client/achievements-{language2}.txt").read().splitlines()

			achievementtitle = translate_messages[72]
			achievementdesc = translate_messages[73]

			embed5 = discord.Embed(title="", color=0x00ff0)
			embed5.add_field(name=f'{achievementtitle}', value=f"{achievementdesc}")
			embed5.set_thumbnail(url="http://clarifygdps.com/geometry-requests/emojies/bug.png")
			return embed5

		def cooldowncheck(author):
			cursor.execute(f"SELECT cooldown FROM cooldowns WHERE userid = {author}")
			try:
				timecheck = cursor.fetchone()[0]
			except TypeError:
				timecheck1 = "2020-11-11 16:55:00"
				timecheck = datetime.datetime.strptime(timecheck1,'%Y-%m-%d %H:%M:%S')
			timecheck = timecheck.timestamp()
			timern = time.time()
			timern = round(timern,0)
			if timern <= timecheck:
				secondcooldown = timecheck-timern
				alwayscooldown = 1
				return alwayscooldown,secondcooldown
			cursor.execute(f"DELETE FROM cooldowns WHERE userid = {author}")
			conn.commit()
			secondcooldown = 0
			alwayscooldown = 0
			return alwayscooldown,secondcooldown
		
		def checkmaintenance(action):
			cursor.execute(f"SELECT {action} FROM maintenance")
			check = cursor.fetchone()[0]
			if check == 1:
				return "yes"
			else:
				return "no"

		await client.change_presence(activity=discord.Streaming(name="req!help | In "+str(len(client.guilds))+" servers!", url="https://www.twitch.tv/joucayt"))
		
		if message.author.id == client.user.id:
			return

		if not message.content.startswith(prefix):
			return

		msg = message.content.split(prefix)[1]
		args = msg.split(" ")
		
		datetime_object = datetime.datetime.now()
		args2 = prefix,' '.join(args)
		channellog = client.get_channel(int(765611422389633064))
		await channellog.send(f"<:requests:726371180508086283> **[{datetime_object}]** __{message.author}__ ({message.author.id}) used the command `{args2}`.")

		if msg.startswith("help"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)
				author = message.author.id

				maincommand = "reqhelp"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqhelp/{language2}.txt").read().splitlines()
				helptitle = translate_messages[0]

				helpinfo1 = translate_messages[1]
				helpinfo2 = translate_messages[2]

				helppublic1 = translate_messages[3]
				helppublic2 = translate_messages[4]
				helppublic3 = translate_messages[5]
				helppublic4 = translate_messages[6]
				helppublic5 = translate_messages[7]
				helppublic6 = translate_messages[8]
				helppublic7 = translate_messages[9]
				helppublic8 = translate_messages[10]
				helppublic9 = translate_messages[11]
				helppublic10 = translate_messages[12]
				helppublic11 = translate_messages[13]

				helpreviewer = translate_messages[14]

				helpadmin1 = translate_messages[15]
				helpadmin2 = translate_messages[16]

				helpgdmod = translate_messages[17]

				helpgrmod1 = translate_messages[18]
				helpgrmod2 = translate_messages[19]
				helpgrmod3 = translate_messages[20]

				helpexample1 = translate_messages[21]
				helpexample2 = translate_messages[22]
				embed = discord.Embed(title=f"{helptitle}", color=0x8E8E8E)
				embed.set_author(name="Geometry Requests", icon_url="https://cdn.discordapp.com/attachments/718241161076146208/718551886499676170/PicsArt_05-10-12.50.41.jpg")
				embed.add_field(name="__Info__", value=f"{helpinfo1}\n{helpinfo2}", inline=False)
				embed.add_field(name="__Public__", value=f"{helppublic1}\n{helppublic2}\n{helppublic3}\n{helppublic4}\n{helppublic5}\n{helppublic6}\n{helppublic7}", inline=False)
				embed.add_field(name="__Public (Page 2)__", value=f"{helppublic8}\n{helppublic9}\n{helppublic10}\n{helppublic11}", inline=False)
				embed.add_field(name="__Reviewers__", value=f"{helpreviewer}", inline=False)
				embed.add_field(name="__Admins__", value=f"{helpadmin1}\n{helpadmin2}", inline=False)
				embed.add_field(name="__GD Moderators__", value=f"{helpgdmod}", inline=False)
				embed.add_field(name="__GR Moderators__", value=f"{helpgrmod1}\n{helpgrmod2}\n{helpgrmod3}", inline=False)
				embed.add_field(name="__Example__", value=f"{helpexample1}\n\n{helpexample2}", inline=False)
				msg = await message.channel.send(embed=embed)
				return

		if msg.startswith("about"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)
				author = message.author.id

				maincommand = "reqabout"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqabout/{language2}.txt").read().splitlines()

				about1 = translate_messages[0]
				about2 = translate_messages[1]
				about3 = translate_messages[2]
				about4 = translate_messages[3]
				about5 = translate_messages[4]
				about6 = translate_messages[5]
				about7 = translate_messages[6]
				about8 = translate_messages[7]
				about9 = translate_messages[8]
				about10 = translate_messages[9]
				about11 = translate_messages[10]

				servernumber = str(len(client.guilds))
				msg = await message.channel.send(f"{about1}\n\n{about2}\n{about3}\n\n{about4}\n\n{about5} {servernumber} {about6}\n\n{about7}\n\n{about8}\n\n{about9}\n\n{about10}\n{about11}")
				return

		if msg.startswith("setup"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor()
				server = message.guild.name
				var = message.guild.id
				author = message.author.id

				maincommand = "reqsetup"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqsetup/{language2}.txt").read().splitlines()

				setupmaintitle = translate_messages[0]
				serversettings = translate_messages[1]

				norole = translate_messages[3]
				nochannel = translate_messages[4]
				notitle = translate_messages[5]
				yestitle = translate_messages[6]

				englishlanguage = translate_messages[8]
				frenchlanguage = translate_messages[9]
				spanishlanguage = translate_messages[10]

				servernametitle = translate_messages[12]
				reviewerroletitle = translate_messages[13]
				ownerroletitle = translate_messages[14]
				requestchanneltitle = translate_messages[15]
				reviewchanneltitle = translate_messages[16]
				checkedreviewchanneltitle = translate_messages[17]
				announcementbottitle = translate_messages[18]
				gdmodchanneltitle = translate_messages[19]
				tagreviewertitle = translate_messages[20]
				needvideotitle = translate_messages[21]
				languagetitle = translate_messages[22]
				removeratedtitle = translate_messages[23]

				errormessage = translate_messages[25]
				erroradmin = translate_messages[26]
				if message.author.guild_permissions.administrator:
					cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
					result = cursor.fetchone()
					embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
					embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
					embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
					reviewerrole = result[2]
					if reviewerrole == None:
						embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
					elif reviewerrole is not None:
						embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
					ownerrole = result[3]
					if ownerrole == None:
						embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
					elif ownerrole is not None:
						embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
					requestchannel = result[4]
					if requestchannel == None:
						embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
					elif requestchannel is not None:
						embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
					reviewchannel = result[5]
					if reviewchannel == None:
						embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
					elif reviewchannel is not None:
						embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
					checkedreviewchannel = result[6]
					if checkedreviewchannel == None:
						embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
					elif checkedreviewchannel is not None:
						embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
					announcementbot = result[7]
					if announcementbot == None:
						embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
					elif announcementbot is not None:
						embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
					conn.commit()
					pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
					gdmod1 = cursor.fetchone()
					if gdmod1 is not None:
						conn.commit()
						cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
						gdmodchannel = result[8]
						if gdmodchannel == None:
							embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
						elif gdmodchannel is not None:
							embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
						gdmodcheckedchannel = result[13]
						if gdmodcheckedchannel == None:
							embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
						elif gdmodcheckedchannel is not None:
							embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
						gdmodcheckedchannelnosend = result[14]
						if gdmodcheckedchannelnosend == None:
							embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
						elif gdmodcheckedchannelnosend is not None:
							embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
					tagreviewer = result[9]
					if tagreviewer == "0":
						embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
					elif tagreviewer == "1":
						embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
					needvideo = result[10]
					if needvideo == "0":
						embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
					elif needvideo == "1":
						embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
					languagesetup = result[11]
					if languagesetup == "en":
						embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
					elif languagesetup == "fr":
						embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
					elif languagesetup == "es":
						embed.add_field(name=f"{languagetitle}", value=f"{spanishlanguage}", inline=False)
					removerated = result[12]
					if removerated == "0":
						embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
					elif removerated == "1":
						embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
                    
					embed.set_footer(text=f"{message.guild.name} --- {message.author}")
					await message.channel.send(embed=embed)
					return
				else:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{erroradmin}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

		if msg.startswith("setconfig"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor()

				maincommand = "reqsetconfig"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				args = [x for ar in args for x in ar.split('\n')]

				try:
					description = args[1].lower()
				except IndexError as error:
					description = None
				try:
					valeur = args[2]
				except IndexError as error:
					valeur = None
				author = message.author.id
				server = message.guild.name

				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqsetconfig/{language2}.txt").read().splitlines()

				setupmaintitle = translate_messages[0]
				serversettings = translate_messages[1]

				norole = translate_messages[3]
				nochannel = translate_messages[4]
				notitle = translate_messages[5]
				yestitle = translate_messages[6]

				englishlanguage = translate_messages[8]
				frenchlanguage = translate_messages[9]
				spanishlanguage = translate_messages[10]

				servernametitle = translate_messages[12]
				reviewerroletitle = translate_messages[13]
				ownerroletitle = translate_messages[14]
				requestchanneltitle = translate_messages[15]
				reviewchanneltitle = translate_messages[16]
				checkedreviewchanneltitle = translate_messages[17]
				announcementbottitle = translate_messages[18]
				gdmodchanneltitle = translate_messages[19]
				tagreviewertitle = translate_messages[20]
				needvideotitle = translate_messages[21]
				languagetitle = translate_messages[22]
				removeratedtitle = translate_messages[23]

				errormessage = translate_messages[25]
				erroradmin = translate_messages[26]

				loadingtitle = translate_messages[28]
				loadingdesc = translate_messages[29]

				errorlink = translate_messages[31]
				errorroledontexist = translate_messages[32]
				errorchanneldontexist = translate_messages[33]
				errorroletag = translate_messages[34]
				errorchanneltag = translate_messages[35]
				errorgdmod = translate_messages[36]
				errorbinary = translate_messages[37]
				errorsetting = translate_messages[38]
				errorlanguage = translate_messages[39]

				cursor.execute(f"SELECT userid FROM users WHERE userid = {author}")
				linked = cursor.fetchone()
				if linked is None:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorlink}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				if message.author.guild_permissions.administrator:
					if description is not None:
						if description == "reviewerrole":
							if valeur is not None:
								if valeur.startswith("<"):
									valeur = valeur.replace('<', '')
									valeur = valeur.replace('>', '')
									valeur = valeur.replace('@', '')
									valeur = valeur.replace('&', '')
									valeur = valeur.replace('!', '')
									roles = discord.utils.get(message.guild.roles)
									role = discord.utils.get(message.guild.roles, id = int(valeur))
									if role is None:
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorroledontexist}")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET ReviewerRole = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorroletag}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						if description == "ownerrole":
							if valeur is not None:
								if valeur.startswith("<"):
									valeur = valeur.replace('<', '')
									valeur = valeur.replace('>', '')
									valeur = valeur.replace('@', '')
									valeur = valeur.replace('&', '')
									valeur = valeur.replace('!', '')
									roles = discord.utils.get(message.guild.roles)
									role = discord.utils.get(message.guild.roles, id = int(valeur))
									if role is None:
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorroledontexist}")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET OwnerRole = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorroletag}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						if description == "requestchannel":
							if valeur is not None:
								if valeur.startswith("<"):
									valeur = valeur.replace('<', '')
									valeur = valeur.replace('>', '')
									valeur = valeur.replace('#', '')
									role = client.get_channel(int(valeur))
									if role is None:
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorchanneldontexist}")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET RequestChannel = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorchanneltag}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						if description == "reviewchannel":
							if valeur is not None:
								if valeur.startswith("<"):
									valeur = valeur.replace('<', '')
									valeur = valeur.replace('>', '')
									valeur = valeur.replace('#', '')
									role = client.get_channel(int(valeur))
									if role is None:
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorchanneldontexist}")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET ReviewChannel = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorchanneltag}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						if description == "checkedreviewchannel":
							if valeur is not None:
								if valeur.startswith("<"):
									valeur = valeur.replace('<', '')
									valeur = valeur.replace('>', '')
									valeur = valeur.replace('#', '')
									role = client.get_channel(int(valeur))
									if role is None:
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorchanneldontexist}")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET CheckedReviewChannel = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorchanneltag}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						if description == "announcementbot":
							if valeur is not None:
								if valeur.startswith("<"):
									valeur = valeur.replace('<', '')
									valeur = valeur.replace('>', '')
									valeur = valeur.replace('#', '')
									role = client.get_channel(int(valeur))
									if role is None:
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorchanneldontexist}")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET AnnouncementBot = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorchanneltag}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						if description == "gdmodchannel":
							var = message.guild.id
							pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
							gdmod1 = cursor.fetchone()
							if gdmod1 is not None:
								if valeur is not None:
									if valeur.startswith("<"):
										valeur = valeur.replace('<', '')
										valeur = valeur.replace('>', '')
										valeur = valeur.replace('#', '')
										role = client.get_channel(int(valeur))
										if role is None:
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorchanneldontexist}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
									var = message.guild.id
									embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
									embed3.add_field(name=f"{loadingdesc}", value="\u200b")
									msg = await message.channel.send(embed=embed3)
									cursor.execute(f"UPDATE setup SET GDModChannel = %s WHERE serverid = {var}", (valeur, ))
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									result = cursor.fetchone()
									await msg.delete()
									embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
									embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
									embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
									reviewerrole = result[2]
									if reviewerrole == None:
										embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
									elif reviewerrole is not None:
										embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
									ownerrole = result[3]
									if ownerrole == None:
										embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
									elif ownerrole is not None:
										embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
									requestchannel = result[4]
									if requestchannel == None:
										embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
									elif requestchannel is not None:
										embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
									reviewchannel = result[5]
									if reviewchannel == None:
										embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
									elif reviewchannel is not None:
										embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
									checkedreviewchannel = result[6]
									if checkedreviewchannel == None:
										embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
									elif checkedreviewchannel is not None:
										embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
									announcementbot = result[7]
									if announcementbot == None:
										embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
									elif announcementbot is not None:
										embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
									conn.commit()
									pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
									gdmod1 = cursor.fetchone()
									if gdmod1 is not None:
										conn.commit()
										cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
										gdmodchannel = result[8]
										if gdmodchannel == None:
											embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
										elif gdmodchannel is not None:
											embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
										gdmodcheckedchannel = result[13]
										if gdmodcheckedchannel == None:
											embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
										elif gdmodcheckedchannel is not None:
											embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
										gdmodcheckedchannelnosend = result[14]
										if gdmodcheckedchannelnosend == None:
											embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
										elif gdmodcheckedchannelnosend is not None:
											embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
									tagreviewer = result[9]
									if tagreviewer == "0":
										embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
									elif tagreviewer == "1":
										embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
									needvideo = result[10]
									if needvideo == "0":
										embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
									elif needvideo == "1":
										embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
									languagesetup = result[11]
									if languagesetup == "en":
										embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
									elif languagesetup == "fr":
										embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
									elif languagesetup == "es":
										embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
									removerated = result[12]
									if removerated == "0":
										embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
									elif removerated == "1":
										embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
									embed.set_footer(text=f"{message.guild.name} --- {message.author}")
									await message.channel.send(embed=embed)
									return
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorchanneltag}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
							else:
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorgdmod}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
						if description == "gdmodcheckedchannel":
							var = message.guild.id
							pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
							gdmod1 = cursor.fetchone()
							if gdmod1 is not None:
								if valeur is not None:
									if valeur.startswith("<"):
										valeur = valeur.replace('<', '')
										valeur = valeur.replace('>', '')
										valeur = valeur.replace('#', '')
										role = client.get_channel(int(valeur))
										if role is None:
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorchanneldontexist}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
									var = message.guild.id
									embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
									embed3.add_field(name=f"{loadingdesc}", value="\u200b")
									msg = await message.channel.send(embed=embed3)
									cursor.execute(f"UPDATE setup SET GDModCheckedChannel = %s WHERE serverid = {var}", (valeur, ))
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									result = cursor.fetchone()
									await msg.delete()
									embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
									embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
									embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
									reviewerrole = result[2]
									if reviewerrole == None:
										embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
									elif reviewerrole is not None:
										embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
									ownerrole = result[3]
									if ownerrole == None:
										embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
									elif ownerrole is not None:
										embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
									requestchannel = result[4]
									if requestchannel == None:
										embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
									elif requestchannel is not None:
										embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
									reviewchannel = result[5]
									if reviewchannel == None:
										embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
									elif reviewchannel is not None:
										embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
									checkedreviewchannel = result[6]
									if checkedreviewchannel == None:
										embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
									elif checkedreviewchannel is not None:
										embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
									announcementbot = result[7]
									if announcementbot == None:
										embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
									elif announcementbot is not None:
										embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
									conn.commit()
									pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
									gdmod1 = cursor.fetchone()
									if gdmod1 is not None:
										conn.commit()
										cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
										gdmodchannel = result[8]
										if gdmodchannel == None:
											embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
										elif gdmodchannel is not None:
											embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
										gdmodcheckedchannel = result[13]
										if gdmodcheckedchannel == None:
											embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
										elif gdmodcheckedchannel is not None:
											embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
										gdmodcheckedchannelnosend = result[14]
										if gdmodcheckedchannelnosend == None:
											embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
										elif gdmodcheckedchannelnosend is not None:
											embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
									tagreviewer = result[9]
									if tagreviewer == "0":
										embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
									elif tagreviewer == "1":
										embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
									needvideo = result[10]
									if needvideo == "0":
										embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
									elif needvideo == "1":
										embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
									languagesetup = result[11]
									if languagesetup == "en":
										embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
									elif languagesetup == "fr":
										embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
									elif languagesetup == "es":
										embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
									removerated = result[12]
									if removerated == "0":
										embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
									elif removerated == "1":
										embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
									embed.set_footer(text=f"{message.guild.name} --- {message.author}")
									await message.channel.send(embed=embed)
									return
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorchanneltag}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
							else:
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorgdmod}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
						if description == "gdmodcheckedchannelnosend":
							var = message.guild.id
							pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
							gdmod1 = cursor.fetchone()
							if gdmod1 is not None:
								if valeur is not None:
									if valeur.startswith("<"):
										valeur = valeur.replace('<', '')
										valeur = valeur.replace('>', '')
										valeur = valeur.replace('#', '')
										role = client.get_channel(int(valeur))
										if role is None:
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorchanneldontexist}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
									var = message.guild.id
									embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
									embed3.add_field(name=f"{loadingdesc}", value="\u200b")
									msg = await message.channel.send(embed=embed3)
									cursor.execute(f"UPDATE setup SET GDModCheckedChannelNoSend = %s WHERE serverid = {var}", (valeur, ))
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									result = cursor.fetchone()
									await msg.delete()
									embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
									embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
									embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
									reviewerrole = result[2]
									if reviewerrole == None:
										embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
									elif reviewerrole is not None:
										embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
									ownerrole = result[3]
									if ownerrole == None:
										embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
									elif ownerrole is not None:
										embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
									requestchannel = result[4]
									if requestchannel == None:
										embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
									elif requestchannel is not None:
										embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
									reviewchannel = result[5]
									if reviewchannel == None:
										embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
									elif reviewchannel is not None:
										embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
									checkedreviewchannel = result[6]
									if checkedreviewchannel == None:
										embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
									elif checkedreviewchannel is not None:
										embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
									announcementbot = result[7]
									if announcementbot == None:
										embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
									elif announcementbot is not None:
										embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
									conn.commit()
									pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
									gdmod1 = cursor.fetchone()
									if gdmod1 is not None:
										conn.commit()
										cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
										gdmodchannel = result[8]
										if gdmodchannel == None:
											embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
										elif gdmodchannel is not None:
											embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
										gdmodcheckedchannel = result[13]
										if gdmodcheckedchannel == None:
											embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
										elif gdmodcheckedchannel is not None:
											embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
										gdmodcheckedchannelnosend = result[14]
										if gdmodcheckedchannelnosend == None:
											embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
										elif gdmodcheckedchannelnosend is not None:
											embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
									tagreviewer = result[9]
									if tagreviewer == "0":
										embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
									elif tagreviewer == "1":
										embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
									needvideo = result[10]
									if needvideo == "0":
										embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
									elif needvideo == "1":
										embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
									languagesetup = result[11]
									if languagesetup == "en":
										embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
									elif languagesetup == "fr":
										embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
									elif languagesetup == "es":
										embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
									removerated = result[12]
									if removerated == "0":
										embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
									elif removerated == "1":
										embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
									embed.set_footer(text=f"{message.guild.name} --- {message.author}")
									await message.channel.send(embed=embed)
									return
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorchanneltag}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
							else:
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorgdmod}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
						if description == "tagreviewer":
							if valeur == "1":
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET TagReviewer = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							elif valeur == "0":
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET TagReviewer = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorbinary}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						if description == "needvideo":
							if valeur == "1":
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET NeedVideo = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							elif valeur == "0":
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET NeedVideo = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorbinary}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						if description == "language":
							if valeur == "en":
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET language = 'en' WHERE serverid = {var}")
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							elif valeur == "fr":
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET language = 'fr' WHERE serverid = {var}")
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							elif valeur == "es":
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET language = 'es' WHERE serverid = {var}")
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							else:
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorlanguage}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
						if description == "removerated":
							if valeur == "1":
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET RemoveRated = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							elif valeur == "0":
								var = message.guild.id
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE setup SET RemoveRated = %s WHERE serverid = {var}", (valeur, ))
								conn.commit()
								cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
								result = cursor.fetchone()
								await msg.delete()
								embed = discord.Embed(title=f"{setupmaintitle}", color=0x8E8E8E)
								embed.set_author(name=f"{serversettings}", icon_url="https://cdn.discordapp.com/emojis/472907599361212426.png?v=1")
								embed.add_field(name=f"{servernametitle}", value=f"{server}", inline=False)
								reviewerrole = result[2]
								if reviewerrole == None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"{norole}", inline=False)
								elif reviewerrole is not None:
									embed.add_field(name=f"{reviewerroletitle}", value=f"<@&{reviewerrole}>", inline=False)
								ownerrole = result[3]
								if ownerrole == None:
									embed.add_field(name=f"{ownerroletitle}", value=f"{norole}", inline=False)
								elif ownerrole is not None:
									embed.add_field(name=f"{ownerroletitle}", value=f"<@&{ownerrole}>", inline=False)
								requestchannel = result[4]
								if requestchannel == None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"{nochannel}", inline=False)
								elif requestchannel is not None:
									embed.add_field(name=f"{requestchanneltitle}", value=f"<#{requestchannel}>", inline=False)
								reviewchannel = result[5]
								if reviewchannel == None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif reviewchannel is not None:
									embed.add_field(name=f"{reviewchanneltitle}", value=f"<#{reviewchannel}>", inline=False)
								checkedreviewchannel = result[6]
								if checkedreviewchannel == None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"{nochannel}", inline=False)
								elif checkedreviewchannel is not None:
									embed.add_field(name=f"{checkedreviewchanneltitle}", value=f"<#{checkedreviewchannel}>", inline=False)
								announcementbot = result[7]
								if announcementbot == None:
									embed.add_field(name=f"{announcementbottitle}", value=f"{nochannel}", inline=False)
								elif announcementbot is not None:
									embed.add_field(name=f"{announcementbottitle}", value=f"<#{announcementbot}>", inline=False)
								conn.commit()
								pogya = cursor.execute(f"SELECT serverid FROM GDmoderators WHERE serverid = {var}")
								gdmod1 = cursor.fetchone()
								if gdmod1 is not None:
									conn.commit()
									cursor.execute(f"SELECT * FROM setup WHERE serverid = {var} LIMIT 1")
									gdmodchannel = result[8]
									if gdmodchannel == None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"{nochannel}", inline=False)
									elif gdmodchannel is not None:
										embed.add_field(name=f"{gdmodchanneltitle}", value=f"<#{gdmodchannel}>", inline=False)
									gdmodcheckedchannel = result[13]
									if gdmodcheckedchannel == None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannel is not None:
										embed.add_field(name=f"GDModCheckedChannel =", value=f"<#{gdmodcheckedchannel}>", inline=False)
									gdmodcheckedchannelnosend = result[14]
									if gdmodcheckedchannelnosend == None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"{nochannel}", inline=False)
									elif gdmodcheckedchannelnosend is not None:
										embed.add_field(name=f"GDModCheckedChannelNoSend =", value=f"<#{gdmodcheckedchannelnosend}>", inline=False)
								tagreviewer = result[9]
								if tagreviewer == "0":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{notitle}", inline=False)
								elif tagreviewer == "1":
									embed.add_field(name=f"{tagreviewertitle}", value=f"{yestitle}", inline=False)
								needvideo = result[10]
								if needvideo == "0":
									embed.add_field(name=f"{needvideotitle}", value=f"{notitle}", inline=False)
								elif needvideo == "1":
									embed.add_field(name=f"{needvideotitle}", value=f"{yestitle}", inline=False)
								languagesetup = result[11]
								if languagesetup == "en":
									embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
								elif languagesetup == "fr":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								elif languagesetup == "es":
									embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
								removerated = result[12]
								if removerated == "0":
									embed.add_field(name=f"{removeratedtitle}", value=f"{notitle}", inline=False)
								elif removerated == "1":
									embed.add_field(name=f"{removeratedtitle}", value=f"{yestitle}", inline=False)
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								await message.channel.send(embed=embed)
								return
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorbinary}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						else:
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorsetting}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
					else:
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errorsetting}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
				else:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{erroradmin}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

		if msg.startswith("search"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqsearch"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				args = [x for ar in args for x in ar.split('\n')]

				try:
					level = args[1:]
				except IndexError as error:
					try:
						level = args[1]
					except IndexError as error:
						level = 0
				finally:
					level = ' '.join(level)

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqsearch/{language2}.txt").read().splitlines()

				errormessage = translate_messages[0]
				errorlevel = translate_messages[1]

				searchresult = translate_messages[3]
				by = translate_messages[4]
				desc = translate_messages[5]
				none = translate_messages[6]
				coinstitle = translate_messages[7]
				sizetitle = translate_messages[8]
				newgroundsplay = translate_messages[9]
				downloadsong = translate_messages[10]
				detailledsong = translate_messages[11]
				idleveltitle = translate_messages[12]
				levelversiontitle = translate_messages[13]
				minimumgdver = translate_messages[14]
				objectcount = translate_messages[15]
				lagtitleobject = translate_messages[16]
				youtubelink = translate_messages[17]
				officialsongtitle = translate_messages[18]
				
				translate_cooldown_messages = open(f"language/client/cooldown-{language2}.txt").read().splitlines()
				errorcooldown1 = translate_cooldown_messages[0]
				errorcooldown2 = translate_cooldown_messages[1]
				
				#cooldowncheck(author)
				alwayscooldown,secondcooldown = cooldowncheck(author)
				
				if alwayscooldown == 1:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorcooldown1} {secondcooldown} {errorcooldown2}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				sql = "INSERT INTO cooldowns (userid, cooldown) VALUES (%s, %s)"
				datetime_object_cooldown = datetime_object + datetime.timedelta(seconds=30)
				val = (author, datetime_object_cooldown)
				cursor.execute(sql,val)
				conn.commit()
				
				#reqsearchfirst(level)
				result2 = reqsearchfirst(level)

				try:
					stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
				except:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorlevel}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
					
				embed = discord.Embed(title=f"{searchresult}", color=color)

				description += '=' * (-len(description) % 4)
				base64_bytes = description.encode('ascii')
				
				message_bytes = base64.urlsafe_b64decode(base64_bytes)
				descbase64 = message_bytes.decode('ascii')

				embed.set_thumbnail(url=f"{ratingemote}")
				if int(objectplus) >= 40000:
					embed.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
				elif int(objectplus) <= 39999:
					embed.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

				if int(coins) == 0:
					coinsvalue = f"{none}"
				elif int(coins) == 1:
					coinsvalue = "<:user_coin_unverified:472908993832943631>"
				elif int(coins) == 2:
					coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
				elif int(coins) == 3:
					coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

				try:
					if int(verifiedcoins) == 1:
						if int(coins) == 0:
							coinsvalue = f"{none}"
						elif int(coins) == 1:
							coinsvalue = "<:user_coin:472908993711308800>"
						elif int(coins) == 2:
							coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
						elif int(coins) == 3:
							coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
				except ValueError:
					pass

				embed.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

				#reqsearch2(level)
				try:
					songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
				except ValueError:
					songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

				songlink2 = unquote(f"{songlink}")
				'''if author == jouca:
					#reqsearch3(songid)
					songartist,artistscouted,artistwhitelisted = reqsearch3(songid)'''
				try:
					officialsong2 = int(officialsong)
				except UnboundLocalError:
					embed.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
					'''if author == jouca:
						embed.add_field(name=f'<:diamond:472907644638855168> {detailledsong}', value=f"**{songartist}**\n**{artistwhitelisted}**\n**{artistscouted}**", inline=False)'''
					if int(objectplus) >= 40000:
						if int(objectplus) >= 65535:
							embed.add_field(name='\u200b', value=f"{idleveltitle} {idlevel}\n{levelversiontitle} {version}\n{minimumgdver} {gdversion}\n{objectcount} {objectplus}+\n<:object_overflow:472908865953071115> {lagtitleobject}", inline=False)
						elif int(objectplus) < 65535:
							embed.add_field(name='\u200b', value=f"{idleveltitle} {idlevel}\n{levelversiontitle} {version}\n{minimumgdver} {gdversion}\n{objectcount} {objectplus}\n<:object_overflow:472908865953071115> {lagtitleobject}", inline=False)
					elif int(objectplus) <= 39999:
						embed.add_field(name='\u200b', value=f"{idleveltitle} {idlevel}\n{levelversiontitle} {version}\n{minimumgdver} {gdversion}\n{objectcount} {objectplus}", inline=False)
					msg1 = await message.channel.send(embed=embed)
					return
				else:
					embed.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
					'''if author == jouca:
						embed.add_field(name=f'<:diamond:472907644638855168> {detailledsong}', value=f"**{songartist}**\n**{artistwhitelisted}**\n**{artistscouted}**", inline=False)'''
					if int(objectplus) >= 40000:
						if int(objectplus) >= 65535:
							embed.add_field(name='\u200b', value=f"{idleveltitle} {idlevel}\n{levelversiontitle} {version}\n{minimumgdver} {gdversion}\n{objectcount} {objectplus}+\n:white_check_mark: {officialsongtitle}\n<:object_overflow:472908865953071115> {lagtitleobject}", inline=False)
						elif int(objectplus) < 65535:
							embed.add_field(name='\u200b', value=f"{idleveltitle} {idlevel}\n{levelversiontitle} {version}\n{minimumgdver} {gdversion}\n{objectcount} {objectplus}\n:white_check_mark: {officialsongtitle}\n<:object_overflow:472908865953071115> {lagtitleobject}", inline=False)
					elif int(objectplus) <= 39999:
						embed.add_field(name='\u200b', value=f"{idleveltitle} {idlevel}\n{levelversiontitle} {version}\n{minimumgdver} {gdversion}\n{objectcount} {objectplus}\n:white_check_mark: {officialsongtitle}", inline=False)
					msg1 = await message.channel.send(embed=embed)
					return

		if msg.startswith("level"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)
				jaj = message.author.id
				room = message.channel.id
				serveur = message.guild.id

				maincommand = "reqlevel"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

				args = [x for ar in args for x in ar.split('\n')]

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author} LIMIT 1")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				cursor.execute(f"SELECT language FROM setup WHERE serverid = {serveur} LIMIT 1")
				try:
					language_serveur = cursor.fetchone()[0]
				except TypeError:
					language_serveur = language_default
				language2_serveur = language_serveur
				translate_messages = open(f"language/client/reqlevel/{language2}.txt").read().splitlines()
				translate_messages_server = open(f"language/server/reqlevel/{language2_serveur}.txt").read().splitlines()

				errormessage = translate_messages[0]
				errorlevel = translate_messages[1]

				loadingtitle = translate_messages[3]
				loadingdesc = translate_messages[4]

				errorlink = translate_messages[6]
				errorreviewerrole = translate_messages[7]
				errorlevelalready = translate_messages[8]
				errorreviewchannel = translate_messages[9]
				errorrequestchannel = translate_messages[10]
				errorrequestnotongoodchannel = translate_messages[11]
				errorban = translate_messages[12]
				errorblacklist = translate_messages[13]
				errorvideo = translate_messages[14]
				errorremoverated = translate_messages[15]
				errormaxrequest = translate_messages[16]

				successtitle = translate_messages[18]
				by = translate_messages[19]
				successrequested = translate_messages[20]

				newlevelreq = translate_messages_server[0]
				byserver = translate_messages_server[1]
				
				translate_messages_search = open(f"language/client/reqsearch/{language2}.txt").read().splitlines()

				searchresult = translate_messages_search[3]
				by = translate_messages_search[4]
				desc = translate_messages_search[5]
				none = translate_messages_search[6]
				coinstitle = translate_messages_search[7]
				sizetitle = translate_messages_search[8]
				newgroundsplay = translate_messages_search[9]
				downloadsong = translate_messages_search[10]
				detailledsong = translate_messages_search[11]
				idleveltitle = translate_messages_search[12]
				levelversiontitle = translate_messages_search[13]
				minimumgdver = translate_messages_search[14]
				objectcount = translate_messages_search[15]
				lagtitleobject = translate_messages_search[16]
				youtubelink = translate_messages_search[17]
				officialsongtitle = translate_messages_search[18]
				
				translate_cooldown_messages = open(f"language/client/cooldown-{language2}.txt").read().splitlines()
				errorcooldown1 = translate_cooldown_messages[0]
				errorcooldown2 = translate_cooldown_messages[1]
				
				#cooldowncheck(author)
				alwayscooldown,secondcooldown = cooldowncheck(author)
				
				if alwayscooldown == 1:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorcooldown1} {secondcooldown} {errorcooldown2}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				sql = "INSERT INTO cooldowns (userid, cooldown) VALUES (%s, %s)"
				datetime_object_cooldown = datetime_object + datetime.timedelta(seconds=30)
				val = (author, datetime_object_cooldown)
				cursor.execute(sql,val)
				conn.commit()
				
				substring = "https://"
				try:
					level = args[1]
				except IndexError as error:
					level = 0
				try:
					video = args[2]
				except IndexError as error:
					video = "no"
				#if msg.count(" ") < 1:
					#embed = discord.Embed(title="", color=0xff0000)
					#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
					#embed.add_field(name='Error. <:error:472907618386575370>', value='Please enter a level ID after "req!level"!')
					#msg2 = await message.channel.send(embed=embed)
					#time.sleep(5)
					#await msg2.delete()
					#return
				#elif len(level) > 9:
					#embed = discord.Embed(title="", color=0xff0000)
					#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
					#embed.add_field(name='Error. <:error:472907618386575370>', value="Your ID is too big and doesn't exist. Please enter a correct level ID after 'req!level'!")
					#msg2 = await message.channel.send(embed=embed)
					#time.sleep(5)
					#await msg2.delete()
					#return
				if video.startswith(substring):
					video2 = None
					embed = discord.Embed(title="", color=0x00ff00)


					data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={level}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
					result = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
					if result == "-1":
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errorlevel}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
					cursor.execute(f"SELECT RemoveRated FROM setup WHERE serverid = {serveur} LIMIT 1")
					try:
						removerated = cursor.fetchone()[0]
					except:
						removerated = 0
					#reqsearch(level)
					stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
					if stars != "0" and removerated == "1":
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errorremoverated}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
					embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
					embed.add_field(name=f'{loadingdesc}', value="\u200b")
					msg = await message.channel.send(embed=embed)

					cursor.execute(f"SELECT userid FROM users WHERE userid = {jaj}")
					linked = cursor.fetchone()
					if linked is None:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errorlink}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
					
					cursor.execute(f"SELECT COUNT(levelid) AS NumberOfLevelIDs FROM levels WHERE server = {serveur} AND reviewed = 'no'")
					count = cursor.fetchone()[0]
					if count >= 100:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errormaxrequest}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return

					result = result.split(":")
					levelname = result[3]
					creator = convertinfo("u","n",result[7])
					poggery = cursor.execute(f"SELECT isBlacklist FROM reports WHERE levelid = %s LIMIT 1", (idlevel, ))
					maybe_number2 = cursor.fetchone()
					if maybe_number2 is None:
						poggare = cursor.execute(f"SELECT userid FROM banned WHERE userid = %s LIMIT 1", (jaj, ))
						maybe_number3 = cursor.fetchone()
						if maybe_number3 is None:
							conn.commit()
							poggarere = cursor.execute(f"SELECT RequestChannel FROM setup WHERE serverid = {serveur} LIMIT 1")
							try:
								maybe_number4 = cursor.fetchone()[0]
							except TypeError:
								maybe_number4 = None
							if maybe_number4 == room:
								poggarerere = cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serveur} LIMIT 1")
								try:
									maybe_number5 = cursor.fetchone()[0]
								except TypeError:
									maybe_number5 = None
								if maybe_number5 is not None:
									poggarererere = cursor.execute(f"SELECT ReviewerRole FROM setup WHERE serverid = {serveur} LIMIT 1")
									try:
										maybe_number6 = cursor.fetchone()[0]
									except TypeError:
										maybe_number6 = None
									if maybe_number6 is not None:
										pogagygi = cursor.execute(f"SELECT levelid FROM levels WHERE server = {serveur} AND levelid = %s LIMIT 1", (level, ))
										try:
											zebi = cursor.fetchone()[0]
										except TypeError:
											zebi = None
										if zebi is not None:
											await msg.delete()
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorlevelalready}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
										else:
											conn.commit()
											reviewed = 'no'
											sql = "INSERT INTO levels (levelid, requester, server, video, reviewed, messageid) VALUES (%s, %s, %s, %s, %s, %s)"
											val = (idlevel, message.author.id, message.guild.id, video2, reviewed, 0)
											cursor.execute(sql, val)
											conn.commit()
											embed3 = discord.Embed(title=f'{newlevelreq}', color=0x00ff00)
											embed3.add_field(name=f'`{idlevel}` (**{levelname}** {byserver} **{creator}**)', value='\u200b')
											embed3.set_footer(text=f"{message.guild.name} --- {message.author}")
											if video is not None:
												cursor.execute(f"UPDATE levels SET video = %s WHERE requester = %s AND levelid = %s AND server = %s", (video, jaj, idlevel, serveur))
												conn.commit()
												embed3.add_field(name=f'\nVideo :', value=f"{video}", inline=False)
											await msg.delete()

											embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed.add_field(name=f'`{idlevel}` (**{levelname}** {by} **{creator}**) {successrequested}', value='\u200b')
											embed.set_footer(text=f"{message.guild.name} --- {message.author}")
											msg100 = await message.channel.send(embed=embed)
											
											#reqsearch(level)
											stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
											description += '=' * (-len(description) % 4)
											base64_bytes = description.encode('ascii')
											
											message_bytes = base64.urlsafe_b64decode(base64_bytes)
											descbase64 = message_bytes.decode('ascii')

											embed3.set_thumbnail(url=f"{ratingemote}")
											if int(objectplus) >= 40000:
												embed3.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
											elif int(objectplus) <= 39999:
												embed3.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

											if int(coins) == 0:
												coinsvalue = f"{none}"
											elif int(coins) == 1:
												coinsvalue = "<:user_coin_unverified:472908993832943631>"
											elif int(coins) == 2:
												coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
											elif int(coins) == 3:
												coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

											try:
												if int(verifiedcoins) == 1:
													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin:472908993711308800>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
											except ValueError:
												pass

											embed3.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

											#reqsearch2(level)
											try:
												songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
											except ValueError:
												songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

											songlink2 = unquote(f"{songlink}")
											try:
												officialsong2 = int(officialsong)
											except UnboundLocalError:
												embed3.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
											else:
												embed3.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
											
											channel2 = client.get_channel(int(maybe_number5))
											pogagaga = cursor.execute(f"SELECT TagReviewer FROM setup WHERE serverid = {serveur} LIMIT 1")
											tagreviewer = cursor.fetchone()[0]
											if tagreviewer == "1":
												msgqueue = await channel2.send(f"<@&{maybe_number6}>",embed=embed3)
											elif tagreviewer == "0":
												msgqueue = await channel2.send(embed=embed3)
											msgid = msgqueue.id
											cursor.execute(f"UPDATE levels SET messageid = %s WHERE requester = %s AND levelid = %s AND server = %s", (msgid, jaj, idlevel, serveur))
											conn.commit()
											
											cursor.execute(f"SELECT levelrequestedcount FROM users WHERE userid = {jaj}")
											counted = cursor.fetchone()[0]
											counted = counted + 1
											cursor.execute(f'UPDATE users SET levelrequestedcount = {counted} WHERE userid = {jaj}')
											conn.commit()
											if counted >= 1:
												cursor.execute(f'SELECT requestachievement1 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "no":
													cursor.execute(f'UPDATE users SET requestachievement1 = "yes" WHERE userid = {jaj}')
													conn.commit()
													#requestachievement1(author)
													embed5 = requestachievement1(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
											if counted >= 5:
												cursor.execute(f'SELECT requestachievement5 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "no":
													cursor.execute(f'UPDATE users SET requestachievement5 = "yes" WHERE userid = {jaj}')
													conn.commit()
													#requestachievement5(author)
													embed5 = requestachievement5(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
											if counted >= 10:
												cursor.execute(f'SELECT requestachievement10 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "no":
													cursor.execute(f'UPDATE users SET requestachievement10 = "yes" WHERE userid = {jaj}')
													conn.commit()
													#requestachievement10(author)
													embed5 = requestachievement10(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
											if counted >= 50:
												cursor.execute(f'SELECT requestachievement50 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "no":
													cursor.execute(f'UPDATE users SET requestachievement50 = "yes" WHERE userid = {jaj}')
													conn.commit()
													#requestachievement50(author)
													embed5 = requestachievement50(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
											if counted >= 100:
												cursor.execute(f'SELECT requestachievement100 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "no":
													cursor.execute(f'UPDATE users SET requestachievement100 = "yes" WHERE userid = {jaj}')
													conn.commit()
													#requestachievement100(author)
													embed5 = requestachievement100(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
											return
									else:
										await msg.delete()
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorreviewerrole}")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
								else:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									embed.add_field(name=f'{errormessage}', value=f"{errorreviewchannel}")
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
							elif maybe_number4 is None:
								await msg.delete()
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorrequestchannel}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
							else:
								await msg.delete()
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorrequestnotongoodchannel} <#{maybe_number4}>.")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
						else:
							await msg.delete()
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorban}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
					else:
						numby = maybe_number2[0]
						if numby == 0:
							poggare = cursor.execute(f"SELECT userid FROM banned WHERE userid = {jaj} LIMIT 1")
							maybe_number3 = cursor.fetchone()
							if maybe_number3 is None:
								conn.commit()
								poggarere = cursor.execute(f"SELECT RequestChannel FROM setup WHERE serverid = {serveur} LIMIT 1")
								try:
									maybe_number4 = cursor.fetchone()[0]
								except TypeError:
									maybe_number4 = None
								if maybe_number4 == room:
									poggarerere = cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serveur} LIMIT 1")
									try:
										maybe_number5 = cursor.fetchone()[0]
									except TypeError:
										maybe_number5 = None
									if maybe_number5 is not None:
										poggarererere = cursor.execute(f"SELECT ReviewerRole FROM setup WHERE serverid = {serveur} LIMIT 1")
										try:
											maybe_number6 = cursor.fetchone()[0]
										except TypeError:
											maybe_number6 = None
										if maybe_number6 is not None:
											pogagygi = cursor.execute(f"SELECT levelid FROM levels WHERE server = {serveur} AND levelid = %s LIMIT 1", (idlevel, ))
											try:
												zebi = cursor.fetchone()[0]
											except TypeError:
												zebi = None
											if zebi is not None:
												await msg.delete()
												embed = discord.Embed(title="", color=0xff0000)
												embed.add_field(name=f'{errormessage}', value=f"{errorlevelalready}")
												msg2 = await message.channel.send(embed=embed)
												time.sleep(5)
												await msg2.delete()
												return
											else:
												conn.commit()
												reviewed = 'no'
												sql = "INSERT INTO levels (levelid, requester, server, video, reviewed, messageid) VALUES (%s, %s, %s, %s, %s, %s)"
												val = (idlevel, message.author.id, message.guild.id, video2, reviewed, 0)
												cursor.execute(sql, val)
												conn.commit()
												embed3 = discord.Embed(title=f'{newlevelreq}', color=0x00ff00)
												embed3.add_field(name=f'`{idlevel}` (**{levelname}** {byserver} **{creator}**)', value='\u200b')
												embed3.set_footer(text=f"{message.guild.name} --- {message.author}")
												if video is not None:
													cursor.execute(f"UPDATE levels SET video = %s WHERE requester = %s AND levelid = %s AND server = %s", (video, jaj, idlevel, serveur))
													conn.commit()
													embed3.add_field(name=f'\nVideo :', value=f"{video}", inline=False)
												await msg.delete()

												embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed.add_field(name=f'`{idlevel}` (**{levelname}** {by} **{creator}**) {successrequested}', value='\u200b')
												embed.set_footer(text=f"{message.guild.name} --- {message.author}")
												msg100 = await message.channel.send(embed=embed)
												
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												embed3.set_thumbnail(url=f"{ratingemote}")
												if int(objectplus) >= 40000:
													embed3.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed3.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed3.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed3.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed3.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												channel2 = client.get_channel(int(maybe_number5))
												pogagaga = cursor.execute(f"SELECT TagReviewer FROM setup WHERE serverid = {serveur} LIMIT 1")
												tagreviewer = cursor.fetchone()[0]
												if tagreviewer == "1":
													msgqueue = await channel2.send(f"<@&{maybe_number6}>",embed=embed3)
												elif tagreviewer == "0":
													msgqueue = await channel2.send(embed=embed3)
												msgid = msgqueue.id
												msgid = msgqueue.id
												cursor.execute(f"UPDATE levels SET messageid = %s WHERE requester = %s AND levelid = %s AND server = %s", (msgid, jaj, idlevel, serveur))
												conn.commit()
												
												cursor.execute(f"SELECT levelrequestedcount FROM users WHERE userid = {jaj}")
												counted = cursor.fetchone()[0]
												counted = counted + 1
												cursor.execute(f'UPDATE users SET levelrequestedcount = {counted} WHERE userid = {jaj}')
												conn.commit()
												if counted >= 1:
													cursor.execute(f'SELECT requestachievement1 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "no":
														cursor.execute(f'UPDATE users SET requestachievement1 = "yes" WHERE userid = {jaj}')
														conn.commit()
														#requestachievement1(author)
														embed5 = requestachievement1(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
												if counted >= 5:
													cursor.execute(f'SELECT requestachievement5 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "no":
														cursor.execute(f'UPDATE users SET requestachievement5 = "yes" WHERE userid = {jaj}')
														conn.commit()
														#requestachievement5(author)
														embed5 = requestachievement5(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
												if counted >= 10:
													cursor.execute(f'SELECT requestachievement10 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "no":
														cursor.execute(f'UPDATE users SET requestachievement10 = "yes" WHERE userid = {jaj}')
														conn.commit()
														#requestachievement10(author)
														embed5 = requestachievement10(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
												if counted >= 50:
													cursor.execute(f'SELECT requestachievement50 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "no":
														cursor.execute(f'UPDATE users SET requestachievement50 = "yes" WHERE userid = {jaj}')
														conn.commit()
														#requestachievement50(author)
														embed5 = requestachievement50(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
												if counted >= 100:
													cursor.execute(f'SELECT requestachievement100 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "no":
														cursor.execute(f'UPDATE users SET requestachievement100 = "yes" WHERE userid = {jaj}')
														conn.commit()
														#requestachievement100(author)
														embed5 = requestachievement100(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
												return
										else:
											await msg.delete()
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorreviewerrole}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
									else:
										await msg.delete()
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorreviewchannel}")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
								elif maybe_number4[0] is None:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									embed.add_field(name=f'{errormessage}', value=f"{errorrequestchannel}")
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
								else:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									embed.add_field(name=f'{errormessage}', value=f"{errorrequestnotongoodchannel} <#{maybe_number4}>.")
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
							else:
								await msg.delete()
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorban}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
						else:
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title="", color=0xff0000)
							#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
							embed.add_field(name=f'{errormessage}', value=f'{errorblacklist}')
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
				else:
					video2 = None
					embed = discord.Embed(title="", color=0x00ff00)

					data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={level}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
					result = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
					if result == "-1":
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errorlevel}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
					cursor.execute(f"SELECT RemoveRated FROM setup WHERE serverid = {serveur} LIMIT 1")
					try:
						removerated = cursor.fetchone()[0]
					except:
						removerated = 0
					#reqsearch(level)
					stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
					if stars != "0" and removerated == "1":
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errorremoverated}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
					embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
					embed.add_field(name=f'{loadingdesc}', value="\u200b")
					msg = await message.channel.send(embed=embed)

					cursor.execute(f"SELECT userid FROM users WHERE userid = {jaj}")
					linked = cursor.fetchone()
					if linked is None:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errorlink}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
						
					cursor.execute(f"SELECT COUNT(levelid) AS NumberOfLevelIDs FROM levels WHERE server = {serveur} AND reviewed = 'no'")
					count = cursor.fetchone()[0]
					if count >= 100:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errormaxrequest}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return

					result = result.split(":")
					levelname = result[3]
					creator = convertinfo("u","n",result[7])
					cursor.execute(f"SELECT NeedVideo FROM setup WHERE serverid = {serveur} LIMIT 1")
					needvideo = cursor.fetchone()[0]
					if needvideo == "0":
						poggery = cursor.execute(f"SELECT isBlacklist FROM reports WHERE levelid = %s LIMIT 1", (idlevel, ))
						maybe_number2 = cursor.fetchone()
						if maybe_number2 is None:
							poggare = cursor.execute(f"SELECT userid FROM banned WHERE userid = {jaj} LIMIT 1")
							maybe_number3 = cursor.fetchone()
							if maybe_number3 is None:
								conn.commit()
								poggarere = cursor.execute(f"SELECT RequestChannel FROM setup WHERE serverid = {serveur} LIMIT 1")
								try:
									maybe_number4 = cursor.fetchone()[0]
								except TypeError:
									maybe_number4 = None
								if maybe_number4 == room:
									poggarerere = cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serveur} LIMIT 1")
									try:
										maybe_number5 = cursor.fetchone()[0]
									except TypeError:
										maybe_number5 = None
									if maybe_number5 is not None:
										poggarererere = cursor.execute(f"SELECT ReviewerRole FROM setup WHERE serverid = {serveur} LIMIT 1")
										try:
											maybe_number6 = cursor.fetchone()[0]
										except TypeError:
											maybe_number6 = None
										if maybe_number6 is not None:
											pogagygi = cursor.execute(f"SELECT levelid FROM levels WHERE server = {serveur} AND levelid = %s LIMIT 1", (idlevel, ))
											try:
												zebi = cursor.fetchone()[0]
											except TypeError:
												zebi = None
											if zebi is not None:
												await msg.delete()
												embed = discord.Embed(title="", color=0xff0000)
												embed.add_field(name=f'{errormessage}', value=f"{errorlevelalready}")
												msg2 = await message.channel.send(embed=embed)
												time.sleep(5)
												await msg2.delete()
												return
											else:
												conn.commit()
												reviewed = 'no'
												sql = "INSERT INTO levels (levelid, requester, server, video, reviewed, messageid) VALUES (%s, %s, %s, %s, %s, %s)"
												val = (idlevel, message.author.id, message.guild.id, video2, reviewed, 0)
												cursor.execute(sql, val)
												conn.commit()
												await msg.delete()

												embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed.add_field(name=f'`{idlevel}` (**{levelname}** {by} **{creator}**) {successrequested}', value='\u200b')
												embed.set_footer(text=f"{message.guild.name} --- {message.author}")
												embed3 = discord.Embed(title=f'{newlevelreq}', color=0x00ff00)
												embed3.add_field(name=f'`{idlevel}` (**{levelname}** {byserver} **{creator}**)', value='\u200b')
												embed3.set_footer(text=f"{message.guild.name} --- {message.author}")
												msg100 = await message.channel.send(embed=embed)
												
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												embed3.set_thumbnail(url=f"{ratingemote}")
												if int(objectplus) >= 40000:
													embed3.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed3.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed3.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed3.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed3.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												channel2 = client.get_channel(int(maybe_number5))
												pogagaga = cursor.execute(f"SELECT TagReviewer FROM setup WHERE serverid = {serveur} LIMIT 1")
												tagreviewer = cursor.fetchone()[0]
												if tagreviewer == "1":
													msgqueue = await channel2.send(f"<@&{maybe_number6}>",embed=embed3)
												elif tagreviewer == "0":
													msgqueue = await channel2.send(embed=embed3)
												msgid = msgqueue.id
												cursor.execute(f"UPDATE levels SET messageid = %s WHERE requester = %s AND levelid = %s AND server = %s", (msgid, jaj, idlevel, serveur))
												conn.commit()
												
												cursor.execute(f"SELECT levelrequestedcount FROM users WHERE userid = {jaj}")
												counted = cursor.fetchone()[0]
												counted = counted + 1
												cursor.execute(f'UPDATE users SET levelrequestedcount = {counted} WHERE userid = {jaj}')
												conn.commit()
												if counted >= 1:
													cursor.execute(f'SELECT requestachievement1 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "no":
														cursor.execute(f'UPDATE users SET requestachievement1 = "yes" WHERE userid = {jaj}')
														conn.commit()
														#requestachievement1(author)
														embed5 = requestachievement1(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
												if counted >= 5:
													cursor.execute(f'SELECT requestachievement5 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "no":
														cursor.execute(f'UPDATE users SET requestachievement5 = "yes" WHERE userid = {jaj}')
														conn.commit()
														#requestachievement5(author)
														embed5 = requestachievement5(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
												if counted >= 10:
													cursor.execute(f'SELECT requestachievement10 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "no":
														cursor.execute(f'UPDATE users SET requestachievement10 = "yes" WHERE userid = {jaj}')
														conn.commit()
														#requestachievement10(author)
														embed5 = requestachievement10(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
												if counted >= 50:
													cursor.execute(f'SELECT requestachievement50 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "no":
														cursor.execute(f'UPDATE users SET requestachievement50 = "yes" WHERE userid = {jaj}')
														conn.commit()
														#requestachievement50(author)
														embed5 = requestachievement50(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
												if counted >= 100:
													cursor.execute(f'SELECT requestachievement100 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "no":
														cursor.execute(f'UPDATE users SET requestachievement100 = "yes" WHERE userid = {jaj}')
														conn.commit()
														#requestachievement100(author)
														embed5 = requestachievement100(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
												return
										else:
											await msg.delete()
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorreviewerrole}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
									else:
										await msg.delete()
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorreviewchannel}")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
								elif maybe_number4 is None:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									embed.add_field(name=f'{errormessage}', value=f"{errorrequestchannel}")
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
								else:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									embed.add_field(name=f'{errormessage}', value=f"{errorrequestnotongoodchannel} <#{maybe_number4}>.")
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
							else:
								await msg.delete()
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorban}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
						else:
							numby = maybe_number2[0]
							if numby == 0:
								poggare = cursor.execute(f"SELECT userid FROM banned WHERE userid = {jaj} LIMIT 1")
								maybe_number3 = cursor.fetchone()
								if maybe_number3 is None:
									conn.commit()
									poggarere = cursor.execute(f"SELECT RequestChannel FROM setup WHERE serverid = {serveur} LIMIT 1")
									try:
										maybe_number4 = cursor.fetchone()[0]
									except TypeError:
										maybe_number4 = None
									if maybe_number4 == room:
										poggarerere = cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serveur} LIMIT 1")
										try:
											maybe_number5 = cursor.fetchone()[0]
										except TypeError:
											maybe_number5 = None
										if maybe_number5 is not None:
											poggarererere = cursor.execute(f"SELECT ReviewerRole FROM setup WHERE serverid = {serveur} LIMIT 1")
											try:
												maybe_number6 = cursor.fetchone()[0]
											except TypeError:
												maybe_number6 = None
											if maybe_number6 is not None:
												pogagygi = cursor.execute(f"SELECT levelid FROM levels WHERE server = {serveur} AND levelid = %s LIMIT 1", (idlevel, ))
												try:
													zebi = cursor.fetchone()[0]
												except TypeError:
													zebi = None
												if zebi is not None:
													await msg.delete()
													embed = discord.Embed(title="", color=0xff0000)
													embed.add_field(name=f'{errormessage}', value=f"{errorlevelalready}")
													msg2 = await message.channel.send(embed=embed)
													time.sleep(5)
													await msg2.delete()
													return
												else:
													conn.commit()
													reviewed = 'no'
													sql = "INSERT INTO levels (levelid, requester, server, video, reviewed, messageid) VALUES (%s, %s, %s, %s, %s, %s)"
													val = (idlevel, message.author.id, message.guild.id, video2, reviewed, 0)
													cursor.execute(sql, val)
													conn.commit()
													embed3 = discord.Embed(title=f'{newlevelreq}', color=0x00ff00)
													embed3.add_field(name=f'`{idlevel}` (**{levelname}** {byserver} **{creator}**)', value='\u200b')
													embed3.set_footer(text=f"{message.guild.name} --- {message.author}")
													if video is not None:
														cursor.execute(f"UPDATE levels SET video = %s WHERE requester = %s AND levelid = %s AND server = %s", (video, jaj, idlevel, serveur))
														conn.commit()
														embed3.add_field(name=f'\nVideo :', value=f"{video}", inline=False)
													await msg.delete()

													embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
													embed.add_field(name=f'`{idlevel}` (**{levelname}** {by} **{creator}**) {successrequested}', value='\u200b')
													embed.set_footer(text=f"{message.guild.name} --- {message.author}")
													msg100 = await message.channel.send(embed=embed)
													
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													embed3.set_thumbnail(url=f"{ratingemote}")
													if int(objectplus) >= 40000:
														embed3.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed3.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed3.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed3.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed3.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)

													channel2 = client.get_channel(int(maybe_number5))
													pogagaga = cursor.execute(f"SELECT TagReviewer FROM setup WHERE serverid = {serveur} LIMIT 1")
													tagreviewer = cursor.fetchone()[0]
													if tagreviewer == "1":
														msgqueue = await channel2.send(f"<@&{maybe_number6}>",embed=embed3)
													elif tagreviewer == "0":
														msgqueue = await channel2.send(embed=embed3)
													msgid = msgqueue.id
													cursor.execute(f"UPDATE levels SET messageid = %s WHERE requester = %s AND levelid = %s AND server = %s", (msgid, jaj, idlevel, serveur))
													conn.commit()
													
													cursor.execute(f"SELECT levelrequestedcount FROM users WHERE userid = {jaj}")
													counted = cursor.fetchone()[0]
													counted = counted + 1
													cursor.execute(f'UPDATE users SET levelrequestedcount = {counted} WHERE userid = {jaj}')
													conn.commit()
													if counted >= 1:
														cursor.execute(f'SELECT requestachievement1 FROM users WHERE userid = {jaj}')
														yesvalue = cursor.fetchone()[0]
														if yesvalue == "no":
															cursor.execute(f'UPDATE users SET requestachievement1 = "yes" WHERE userid = {jaj}')
															conn.commit()
															#requestachievement1(author)
															embed5 = requestachievement1(author)
															username = await client.fetch_user(int(jaj))
															channel = await username.create_dm()
															try:
																await channel.send(embed=embed5)
															except discord.errors.Forbidden:
																pass
													if counted >= 5:
														cursor.execute(f'SELECT requestachievement5 FROM users WHERE userid = {jaj}')
														yesvalue = cursor.fetchone()[0]
														if yesvalue == "no":
															cursor.execute(f'UPDATE users SET requestachievement5 = "yes" WHERE userid = {jaj}')
															conn.commit()
															#requestachievement5(author)
															embed5 = requestachievement5(author)
															username = await client.fetch_user(int(jaj))
															channel = await username.create_dm()
															try:
																await channel.send(embed=embed5)
															except discord.errors.Forbidden:
																pass
													if counted >= 10:
														cursor.execute(f'SELECT requestachievement10 FROM users WHERE userid = {jaj}')
														yesvalue = cursor.fetchone()[0]
														if yesvalue == "no":
															cursor.execute(f'UPDATE users SET requestachievement10 = "yes" WHERE userid = {jaj}')
															conn.commit()
															#requestachievement10(author)
															embed5 = requestachievement10(author)
															username = await client.fetch_user(int(jaj))
															channel = await username.create_dm()
															try:
																await channel.send(embed=embed5)
															except discord.errors.Forbidden:
																pass
													if counted >= 50:
														cursor.execute(f'SELECT requestachievement50 FROM users WHERE userid = {jaj}')
														yesvalue = cursor.fetchone()[0]
														if yesvalue == "no":
															cursor.execute(f'UPDATE users SET requestachievement50 = "yes" WHERE userid = {jaj}')
															conn.commit()
															#requestachievement50(author)
															embed5 = requestachievement50(author)
															username = await client.fetch_user(int(jaj))
															channel = await username.create_dm()
															try:
																await channel.send(embed=embed5)
															except discord.errors.Forbidden:
																pass
													if counted >= 100:
														cursor.execute(f'SELECT requestachievement100 FROM users WHERE userid = {jaj}')
														yesvalue = cursor.fetchone()[0]
														if yesvalue == "no":
															cursor.execute(f'UPDATE users SET requestachievement100 = "yes" WHERE userid = {jaj}')
															conn.commit()
															#requestachievement100(author)
															embed5 = requestachievement100(author)
															username = await client.fetch_user(int(jaj))
															channel = await username.create_dm()
															try:
																await channel.send(embed=embed5)
															except discord.errors.Forbidden:
																pass
													return
											else:
												await msg.delete()
												embed = discord.Embed(title="", color=0xff0000)
												embed.add_field(name=f'{errormessage}', value=f"{errorreviewerrole}")
												msg2 = await message.channel.send(embed=embed)
												time.sleep(5)
												await msg2.delete()
												return
										else:
											await msg.delete()
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorrequestchannel}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
									elif maybe_number4[0] is None:
										await msg.delete()
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorrequestchannel}")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
									else:
										await msg.delete()
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorrequestnotongoodchannel} <#{maybe_number4}>.")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
								else:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									embed.add_field(name=f'{errormessage}', value=f"{errorban}")
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
							else:
								conn.commit()
								await msg.delete()
								embed = discord.Embed(title="", color=0xff0000)
								#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
								embed.add_field(name=f'{errormessage}', value=f'{errorblacklist}')
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
					else:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errorvideo}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return

		if msg.startswith("queue"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor(buffered=True)
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				author = message.author.id
				serverid = message.guild.id

				maincommand = "reqqueue"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqqueue/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				queuetitle = translate_messages[3]
				queuedesc = translate_messages[4]
				by = translate_messages[5]
				information = translate_messages[6]
				page = translate_messages[7]
				scrollpage = translate_messages[8]
				totallevels = translate_messages[9]
				
				translate_cooldown_messages = open(f"language/client/cooldown-{language2}.txt").read().splitlines()
				errorcooldown1 = translate_cooldown_messages[0]
				errorcooldown2 = translate_cooldown_messages[1]
				errormessage = translate_cooldown_messages[3]
				
				#cooldowncheck(author)
				alwayscooldown,secondcooldown = cooldowncheck(author)
				
				if alwayscooldown == 1:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorcooldown1} {secondcooldown} {errorcooldown2}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				sql = "INSERT INTO cooldowns (userid, cooldown) VALUES (%s, %s)"
				datetime_object_cooldown = datetime_object + datetime.timedelta(seconds=30)
				val = (author, datetime_object_cooldown)
				cursor.execute(sql,val)
				conn.commit()

				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)

				var = message.guild.id

				cursor.execute("SELECT levelid,video FROM levels WHERE server = {} AND reviewed = 'no' ORDER BY ID ASC LIMIT 100".format(var))
				datas = cursor.fetchall()
				levels = []
				creators = []

				for k in range(len(datas)):
					levels.append(str(datas[k][0]))

				result = queuedecryptor(levels)

				embed400 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed400.add_field(name=f'{queuedesc}', value="\u200b", inline=False)

				if len(levels) == 0:
					await msg.delete()
					msg1 = await message.channel.send(embed=embed400)
					return

				# Getting level datas
				levels = []
				result = result.split("#")
				result1 = result[0]
				#Getting Username
				result2 = result[1]
				result = result1.split("|")

				result2 = result2.split("|")

				for g in range(len(result)):
					levelids = result[g]
					levelids = levelids.split(":")
					levels.append(levelids[1])
					for k in range(len(result2)):
						accountid = result2[k]
						accountid = accountid.split(":")
						if levelids[7] == accountid[0]:
							creatornamed = result2[k]
							creatornamed = creatornamed.split(":")
							creators.append(creatornamed[1])
							break

				minpage = 0
				maxpage = round((len(levels)+5-1) // 5)

				pageselect = 0
				current = 1
				maxshow = 5

				totallevelsresult = len(levels)

				embed1 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed1.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed1.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed2 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed2.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed2.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed3 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed3.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed3.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed4 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed4.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed4.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed5 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed5.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed5.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed6 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed6.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed6.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed7 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed7.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed7.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed8 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed8.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed8.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed9 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed9.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed9.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed10 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed10.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed10.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed11 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed11.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed11.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed12 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed12.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed12.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed13 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed13.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed13.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed14 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed14.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed14.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed15 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed15.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed15.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed16 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed16.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed16.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed17 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed17.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed17.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed18 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed18.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed18.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed19 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed19.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed19.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed20 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed20.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed20.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)

				iconprofile = message.guild.icon_url
				embed1.set_thumbnail(url=(iconprofile))

				if result == "-1":
					await msg.delete()
					msg1 = await message.channel.send(embed=embed1)
					return

				pages = [embed1,embed2,embed3,embed4,embed5,embed6,embed7,embed8,embed9,embed10,embed11,embed12,embed13,embed14,embed15,embed16,embed17,embed18,embed19,embed20]
				
				datatest = datas
				o=-1
				for l in range(len(datatest)):
					o+=1
					if str(datatest[o][0]) not in levels:
						del datatest[o]
						o-=1

				for h in range(len(result)):
					video = datatest[h][1]
					if current > maxshow:
						maxshow += 5
						pageselect += 1
						pages[pageselect].set_thumbnail(url=(iconprofile))	
					current += 1
					queueconstructor(pageselect,result[h],video,h+1,levels[h],pages,creators[h])

				def check(reaction, user):
					return user == message.author

				i = 0
				reaction = None

				await msg.delete()
				msg1 = await message.channel.send(embed=embed1)

				if pageselect <= 1:
					return

				await msg1.add_reaction(right)

				while True:
					if str(reaction) == right:
						i += 1
						if i+1>=maxpage:
							await msg1.clear_reactions()
							await msg1.add_reaction(left)
							await msg1.edit(embed = pages[i])
						else:
							await msg1.add_reaction(left)
							await msg1.add_reaction(right)
							await msg1.edit(embed = pages[i])
					if str(reaction) == left:
						i -= 1
						if i<=minpage:
							await msg1.clear_reactions()
							await msg1.add_reaction(right)
							await msg1.edit(embed = pages[i])
						else:
							await msg1.add_reaction(left)
							await msg1.add_reaction(right)
							await msg1.edit(embed = pages[i])

					try:
						reaction, user = await client.wait_for('reaction_add', timeout = 15.0, check = check)
						await msg1.remove_reaction(reaction, user)
					except:
						break
				await msg1.clear_reactions()
				return

		if msg.startswith("modqueue"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor(buffered=True)
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				author = message.author.id
				serverid = message.guild.id

				maincommand = "reqmodqueue"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqmodqueue/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				queuetitle = translate_messages[3]
				queuedesc = translate_messages[4]
				by = translate_messages[5]
				information = translate_messages[6]
				page = translate_messages[7]
				scrollpage = translate_messages[8]
				totallevels = translate_messages[9]

				errorpermission = translate_messages[11]
				
				translate_cooldown_messages = open(f"language/client/cooldown-{language2}.txt").read().splitlines()
				errorcooldown1 = translate_cooldown_messages[0]
				errorcooldown2 = translate_cooldown_messages[1]
				errormessage = translate_cooldown_messages[3]
				
				#cooldowncheck(author)
				alwayscooldown,secondcooldown = cooldowncheck(author)
				
				if alwayscooldown == 1:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorcooldown1} {secondcooldown} {errorcooldown2}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				sql = "INSERT INTO cooldowns (userid, cooldown) VALUES (%s, %s)"
				datetime_object_cooldown = datetime_object + datetime.timedelta(seconds=30)
				val = (author, datetime_object_cooldown)
				cursor.execute(sql,val)
				conn.commit()

				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)

				cursor.execute(f"SELECT userid FROM GDmoderators WHERE userid = {author} LIMIT 1")
				gdmod = cursor.fetchone()
				if gdmod is None:
					await msg.delete()
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorpermission}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

				var = message.guild.id

				cursor.execute("SELECT levelid,video FROM levels WHERE server = {} AND reviewed = 'yes' ORDER BY messageid ASC LIMIT 100".format(var))
				datas = cursor.fetchall()
				levels = []
				creators = []

				for k in range(len(datas)):
					levels.append(str(datas[k][0]))

				embed400 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed400.add_field(name=f'{queuedesc}', value="\u200b", inline=False)

				if len(levels) == 0:
					await msg.delete()
					msg1 = await message.channel.send(embed=embed400)
					return

				result = queuedecryptor(levels)

				# Getting level datas
				levels = []
				result = result.split("#")
				result1 = result[0]
				#Getting Username
				result2 = result[1]
				result = result1.split("|")

				result2 = result2.split("|")

				for g in range(len(result)):
					levelids = result[g]
					levelids = levelids.split(":")
					levels.append(levelids[1])
					for k in range(len(result2)):
						accountid = result2[k]
						accountid = accountid.split(":")
						if levelids[7] == accountid[0]:
							creatornamed = result2[k]
							creatornamed = creatornamed.split(":")
							creators.append(creatornamed[1])
							break

				minpage = 0
				maxpage = round((len(levels)+5-1) // 5)

				pageselect = 0
				current = 1
				maxshow = 5

				totallevelsresult = len(levels)

				embed1 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed1.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed1.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed2 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed2.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed2.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed3 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed3.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed3.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed4 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed4.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed4.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed5 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed5.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed5.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed6 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed6.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed6.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed7 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed7.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed7.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed8 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed8.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed8.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed9 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed9.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed9.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed10 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed10.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed10.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed11 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed11.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed11.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed12 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed12.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed12.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed13 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed13.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed13.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed14 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed14.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed14.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed15 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed15.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed15.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed16 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed16.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed16.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed17 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed17.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed17.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed18 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed18.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed18.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed19 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed19.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed19.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed20 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed20.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed20.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)

				iconprofile = message.guild.icon_url
				embed1.set_thumbnail(url=(iconprofile))

				if result == "-1":
					await msg.delete()
					msg1 = await message.channel.send(embed=embed1)
					return

				pages = [embed1,embed2,embed3,embed4,embed5,embed6,embed7,embed8,embed9,embed10,embed11,embed12,embed13,embed14,embed15,embed16,embed17,embed18,embed19,embed20]
				
				datatest = datas
				o=-1
				for l in range(len(datatest)):
					o+=1
					if str(datatest[o][0]) not in levels:
						del datatest[o]
						o-=1

				for h in range(len(result)):
					video = datatest[h][1]
					if current > maxshow:
						maxshow += 5
						pageselect += 1
						pages[pageselect].set_thumbnail(url=(iconprofile))	
					current += 1
					queueconstructor(pageselect,result[h],video,h+1,levels[h],pages,creators[h])

				def check(reaction, user):
					return user == message.author

				i = 0
				reaction = None

				await msg.delete()
				msg1 = await message.channel.send(embed=embed1)

				if pageselect <= 1:
					return

				await msg1.add_reaction(right)

				while True:
					if str(reaction) == right:
						i += 1
						if i+1>=maxpage:
							await msg1.clear_reactions()
							await msg1.add_reaction(left)
							await msg1.edit(embed = pages[i])
						else:
							await msg1.add_reaction(left)
							await msg1.add_reaction(right)
							await msg1.edit(embed = pages[i])
					if str(reaction) == left:
						i -= 1
						if i<=minpage:
							await msg1.clear_reactions()
							await msg1.add_reaction(right)
							await msg1.edit(embed = pages[i])
						else:
							await msg1.add_reaction(left)
							await msg1.add_reaction(right)
							await msg1.edit(embed = pages[i])

					try:
						reaction, user = await client.wait_for('reaction_add', timeout = 15.0, check = check)
						await msg1.remove_reaction(reaction, user)
					except:
						break
				await msg1.clear_reactions()
				return

		if msg.startswith("myqueue"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor(buffered=True)
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				author = message.author.id
				serverid = message.guild.id

				maincommand = "reqmyqueue"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqmyqueue/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				queuetitle = translate_messages[3]
				queuedesc = translate_messages[4]
				by = translate_messages[5]
				information = translate_messages[6]
				page = translate_messages[7]
				scrollpage = translate_messages[8]
				requestedserver = translate_messages[9]
				totallevels = translate_messages[10]
				
				translate_cooldown_messages = open(f"language/client/cooldown-{language2}.txt").read().splitlines()
				errormessage123 = translate_cooldown_messages[3]
				errorcooldown1 = translate_cooldown_messages[0]
				errorcooldown2 = translate_cooldown_messages[1]
				
				#cooldowncheck(author)
				alwayscooldown,secondcooldown = cooldowncheck(author)
				
				if alwayscooldown == 1:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage123}', value=f"{errorcooldown1} {secondcooldown} {errorcooldown2}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				sql = "INSERT INTO cooldowns (userid, cooldown) VALUES (%s, %s)"
				datetime_object_cooldown = datetime_object + datetime.timedelta(seconds=30)
				val = (author, datetime_object_cooldown)
				cursor.execute(sql,val)
				conn.commit()
				
				userid = message.author.id
				var = message.guild.id
				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)

				requester = message.author.id

				cursor.execute("SELECT levelid,video,server FROM levels WHERE requester = {} AND reviewed = 'no' ORDER BY ID ASC LIMIT 100".format(requester))
				datas = cursor.fetchall()
				levels = []
				creators = []

				for k in range(len(datas)):
					levels.append(str(datas[k][0]))

				embed400 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed400.add_field(name=f'{queuedesc}', value="\u200b", inline=False)

				if len(levels) == 0:
					await msg.delete()
					msg1 = await message.channel.send(embed=embed400)
					return

				result = queuedecryptor(levels)

				minpage = 0
				maxpage = round((len(levels)+5-1) // 5)

				pageselect = 0
				current = 1
				maxshow = 5

				totallevelsresult = len(levels)

				# Getting level datas
				levels = []
				result = result.split("#")
				result1 = result[0]
				#Getting Username
				result2 = result[1]
				result = result1.split("|")

				result2 = result2.split("|")

				for g in range(len(result)):
					levelids = result[g]
					levelids = levelids.split(":")
					levels.append(levelids[1])
					for k in range(len(result2)):
						accountid = result2[k]
						accountid = accountid.split(":")
						if levelids[7] == accountid[0]:
							creatornamed = result2[k]
							creatornamed = creatornamed.split(":")
							creators.append(creatornamed[1])
							break

				embed1 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed1.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed1.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed2 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed2.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed2.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed3 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed3.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed3.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed4 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed4.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed4.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed5 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed5.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed5.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed6 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed6.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed6.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed7 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed7.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed7.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed8 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed8.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed8.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed9 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed9.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed9.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed10 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed10.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed10.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed11 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed11.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed11.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed12 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed12.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed12.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed13 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed13.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed13.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed14 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed14.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed14.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed15 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed15.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed15.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed16 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed16.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed16.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed17 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed17.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed17.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed18 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed18.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed18.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed19 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed19.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed19.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)
				embed20 = discord.Embed(title=f"{queuetitle} "+str(message.guild.name), color=0x00ff00)
				embed20.add_field(name=f'{queuedesc}', value="\u200b", inline=False)
				embed20.add_field(name=f'{totallevels} {totallevelsresult}', value="\u200b", inline=False)

				usera = await message.guild.fetch_member(requester)
				iconprofile = usera.avatar_url
				embed1.set_thumbnail(url=(iconprofile))

				if result == "-1":
					await msg.delete()
					msg1 = await message.channel.send(embed=embed1)
					return

				pages = [embed1,embed2,embed3,embed4,embed5,embed6,embed7,embed8,embed9,embed10,embed11,embed12,embed13,embed14,embed15,embed16,embed17,embed18,embed19,embed20]
				
				datatest = datas
				o=-1
				for l in range(len(datatest)):
					o+=1
					if str(datatest[o][0]) not in levels:
						del datatest[o]
						o-=1
				
				for h in range(len(result)):
					video = datas[h][1]
					if current > maxshow:
						maxshow += 5
						pageselect += 1
						pages[pageselect].set_thumbnail(url=(iconprofile))	
					current += 1
					myqueueconstructor(pageselect,result[h],video,h+1,levels[h],pages,var,creators[h])

				def check(reaction, user):
					return user == message.author

				i = 0
				reaction = None

				await msg.delete()
				msg1 = await message.channel.send(embed=embed1)

				if pageselect <= 1:
					return

				await msg1.add_reaction(right)

				while True:
					if str(reaction) == right:
						i += 1
						if i+1>=maxpage:
							await msg1.clear_reactions()
							await msg1.add_reaction(left)
							await msg1.edit(embed = pages[i])
						else:
							await msg1.add_reaction(left)
							await msg1.add_reaction(right)
							await msg1.edit(embed = pages[i])
					if str(reaction) == left:
						i -= 1
						if i<=minpage:
							await msg1.clear_reactions()
							await msg1.add_reaction(right)
							await msg1.edit(embed = pages[i])
						else:
							await msg1.add_reaction(left)
							await msg1.add_reaction(right)
							await msg1.edit(embed = pages[i])

					try:
						reaction, user = await client.wait_for('reaction_add', timeout = 15.0, check = check)
						await msg1.remove_reaction(reaction, user)
					except:
						break
				await msg1.clear_reactions()
				return

		if msg.startswith("review"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqreview"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				args = [x for ar in args for x in ar.split('\n')]

				try:
					level = args[1]
				except IndexError as error:
					level = 0
				try:
					validation = args[2]
				except IndexError as error:
					validation = None
				try:
					feedback = args[3:]
				except IndexError as error:
					feedback = None
				serverid = message.guild.id
				servername = message.guild.name
				jaj = message.author.id

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqreview/{language2}.txt").read().splitlines()

				cursor.execute(f"SELECT language FROM setup WHERE serverid = {serverid}")
				try:
					language_serveur = cursor.fetchone()[0]
				except TypeError:
					language_serveur = language_default
				language2_serveur = language_serveur
				translate_messages_server = open(f"language/server/reqreview/{language2_serveur}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorlink = translate_messages[4]
				errorcheckedreviewchannel = translate_messages[5]
				errorsyntax = translate_messages[6]
				errorban = translate_messages[7]
				errorrequiredrole = translate_messages[8]
				errornotfound1 = translate_messages[9]
				errornotfound2 = translate_messages[10]

				byclient2 = translate_messages[13]

				successtitle = translate_messages[16]
				successreviewed = translate_messages[17]

				leveltitle = translate_messages_server[0]
				byserver = translate_messages_server[1]
				reviewed = translate_messages_server[2]
				reviewedby = translate_messages_server[3]
				gdmodlevelapproved = translate_messages_server[4]

				levelapprovedserver = translate_messages_server[6]
				levelunapprovedserver = translate_messages_server[7]
				
				translate_messages_search = open(f"language/client/reqsearch/{language2}.txt").read().splitlines()

				searchresult = translate_messages_search[3]
				by = translate_messages_search[4]
				desc = translate_messages_search[5]
				none = translate_messages_search[6]
				coinstitle = translate_messages_search[7]
				sizetitle = translate_messages_search[8]
				newgroundsplay = translate_messages_search[9]
				downloadsong = translate_messages_search[10]
				detailledsong = translate_messages_search[11]
				idleveltitle = translate_messages_search[12]
				levelversiontitle = translate_messages_search[13]
				minimumgdver = translate_messages_search[14]
				objectcount = translate_messages_search[15]
				lagtitleobject = translate_messages_search[16]
				youtubelink = translate_messages_search[17]
				officialsongtitle = translate_messages_search[18]
				
				translate_cooldown_messages = open(f"language/client/cooldown-{language2}.txt").read().splitlines()
				errorcooldown1 = translate_cooldown_messages[0]
				errorcooldown2 = translate_cooldown_messages[1]
				
				#cooldowncheck(author)
				alwayscooldown,secondcooldown = cooldowncheck(author)
				
				if alwayscooldown == 1:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorcooldown1} {secondcooldown} {errorcooldown2}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				sql = "INSERT INTO cooldowns (userid, cooldown) VALUES (%s, %s)"
				datetime_object_cooldown = datetime_object + datetime.timedelta(seconds=30)
				val = (author, datetime_object_cooldown)
				cursor.execute(sql,val)
				conn.commit()
				
				data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={level}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
				result = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
				if result == "-1":
					cursor.execute(f"DELETE FROM levels WHERE levelid = %s", (level, ))
					conn.commit()
					embed = discord.Embed(title="", color=0xff0000)
					#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
					embed.add_field(name=f'{errormessage}', value=f'{errornotfound1} `{level}` {errornotfound2}')
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)

				cursor.execute(f"SELECT userid FROM users WHERE userid = {jaj}")
				linked = cursor.fetchone()
				if linked is None:
					await msg.delete()
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorlink}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

				pog = cursor.execute(f"SELECT levelid FROM levels WHERE server = %s AND levelid = %s", (serverid, level))
				maybe_number = cursor.fetchone()
				while maybe_number:
					if str(maybe_number[0]) == level:
						poggery = cursor.execute(f"SELECT ReviewerRole FROM setup WHERE serverid = {serverid} LIMIT 1")
						maybe_number2 = cursor.fetchone()
						role = get(client.get_guild(message.guild.id).roles, id=int(maybe_number2[0]))
						if role in message.author.roles:
							result = result.split(":")
							levelname = result[3]
							creator = convertinfo("u","n",result[7])
							poggare = cursor.execute(f"SELECT userid FROM banned WHERE userid = {jaj} LIMIT 1")
							maybe_number3 = cursor.fetchone()
							if maybe_number3 is None:
								nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = {serverid} LIMIT 1", (level, ))
								user1 = cursor.fetchone()[0]
								username = await client.fetch_user(int(user1))
								if validation == "yes":
									if feedback != []:
										sentence = ' '.join(feedback)
										jojo = cursor.execute(f"SELECT CheckedReviewChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
										try:
											checkedreviewchannel = cursor.fetchone()[0]
										except TypeError:
											checkedreviewchannel = None
										if checkedreviewchannel is not None:
											channel2 = client.get_channel(int(checkedreviewchannel))
											pogya = cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmod = cursor.fetchone()[0]
											except TypeError:
												gdmod = None
											if gdmod is not None:
												embed2 = discord.Embed(title=f'{leveltitle} {levelname} {byserver} {creator} (`{level}`) {reviewed} <:downloads:472907713727430658>', description=f"<:success:472908961176092702> - {sentence}", color=0x00ff00)
												
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												embed2.set_thumbnail(url=f"{ratingemote}")
												if int(objectplus) >= 40000:
													embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed2.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed2.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed2.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												embed2.set_footer(text=f"{reviewedby} {message.author}")
												await channel2.send(f"<@{user1}>",embed=embed2)
												cursor.execute(f"UPDATE levels SET reviewed = 'yes' WHERE levelid = %s AND server = {serverid}", (level, ))
												channel = await username.create_dm()

												cursor.execute(f"SELECT language FROM users WHERE userid = %s", (user1, ))
												try:
													language_author = cursor.fetchone()[0]
												except TypeError:
													language_author = language_default
												language22 = language
												translate2_messages = open(f"language/client/reqreview/{language22}.txt").read().splitlines()

												yourlevel = translate2_messages[12]
												byclient = translate2_messages[13]
												havebeenreviewed = translate2_messages[14]

												try:
													await channel.send(f"{yourlevel} {levelname} {byclient} {creator} {havebeenreviewed} `{servername}` !",embed=embed2)
												except discord.errors.Forbidden:
													pass
												await msg.delete()
												
												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												msg101 = await channelmessageid.fetch_message(int(messages))

												try:
													await msg101.delete()
												except:
													pass
												
												embed3 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed3.add_field(name=f'`{level}` (**{levelname}** {byclient2} **{creator}**) {successreviewed}', value='\u200b')
												await message.channel.send(embed=embed3)
												pognya = cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												gdmodchannel123 = cursor.fetchone()
												channel3 = client.get_channel(int(gdmodchannel123[0]))
												embed4 = discord.Embed(title=f'{gdmodlevelapproved}', color=0x00ff00)
												embed4.add_field(name=f'`{level}` (**{levelname}** {byserver} **{creator}**)', value='\u200b')

												cursor.execute(f"SELECT video FROM levels WHERE server = {serverid} AND levelid = {level}")
												videotype = cursor.fetchone()[0]
												if videotype is not None:
													embed4.add_field(name=f'\nVideo :', value=f"{videotype}", inline=False)
												
												pognyanya = cursor.execute(f"SELECT userid FROM GDmoderators WHERE serverid = {serverid} LIMIT 1")
												gdmodchannel1234 = cursor.fetchone()
												msgmod = await channel3.send(f"<@{gdmodchannel1234[0]}>",embed=embed4)
												msgmod2 = getattr(msgmod,"id")
												
												cursor.execute(f"UPDATE levels SET messageid = {msgmod2} WHERE server = {serverid} AND levelid = {level}")
												conn.commit()

												cursor.execute(f"SELECT levelreviewedcount FROM users WHERE userid = {jaj}")
												counted = cursor.fetchone()[0]
												counted = counted + 1
												cursor.execute(f'UPDATE users SET levelreviewedcount = {counted} WHERE userid = {jaj}')
												conn.commit()
												if counted >= 1:
													cursor.execute(f'SELECT reviewachievement1 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement1 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement1(author)
														embed5 = reviewachievement1(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 5:
													cursor.execute(f'SELECT reviewachievement5 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement5 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement5(author)
														embed5 = reviewachievement5(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 10:
													cursor.execute(f'SELECT reviewachievement10 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement10 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement10(author)
														embed5 = reviewachievement10(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 50:
													cursor.execute(f'SELECT reviewachievement50 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement50 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement50(author)
														embed5 = reviewachievement50(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 100:
													cursor.execute(f'SELECT reviewachievement100 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement100 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement100(author)
														embed5 = reviewachievement100(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass

												cursor.execute(f"SELECT levelreviewapprovedcount FROM users WHERE userid = %s", (user1, ))
												counted2 = cursor.fetchone()[0]
												counted2 += 1
												cursor.execute(f'UPDATE users SET levelreviewapprovedcount = {counted2} WHERE userid = %s', (user1, ))
												conn.commit()
												if counted2 >= 1:
													cursor.execute(f'SELECT reviewapprovedachievement1 FROM users WHERE userid = %s', (user1, ))
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement1 = "yes" WHERE userid = %s', (user1, ))
														conn.commit()
														reviewapprovedachievement1(user1)
														embed5 = reviewapprovedachievement1(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 5:
													cursor.execute(f'SELECT reviewapprovedachievement5 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement5 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement5(user1)
														embed5 = reviewapprovedachievement5(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 10:
													cursor.execute(f'SELECT reviewapprovedachievement10 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement10 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement10(user1)
														embed5 = reviewapprovedachievement10(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 50:
													cursor.execute(f'SELECT reviewapprovedachievement50 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement50 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement50(user1)
														embed5 = reviewapprovedachievement50(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 100:
													cursor.execute(f'SELECT reviewapprovedachievement100 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement100 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement100(user1)
														embed5 = reviewapprovedachievement100(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												return
											else:
												embed2 = discord.Embed(title=f'{leveltitle} {levelname} {byserver} {creator} (`{level}`) {reviewed} <:downloads:472907713727430658>', description=f"<:success:472908961176092702> - {sentence}", color=0x00ff00)
												
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												embed2.set_thumbnail(url=f"{ratingemote}")
												if int(objectplus) >= 40000:
													embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed2.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed2.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed2.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												embed2.set_footer(text=f"{reviewedby} {message.author}")
												await channel2.send(f"<@{user1}>",embed=embed2)
												channel = await username.create_dm()

												cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
												try:
													language_author = cursor.fetchone()[0]
												except TypeError:
													language_author = language_default
												language22 = language
												translate2_messages = open(f"language/client/reqreview/{language22}.txt").read().splitlines()

												yourlevel = translate2_messages[12]
												byclient = translate2_messages[13]
												havebeenreviewed = translate2_messages[14]

												try:
													await channel.send(f"{yourlevel} {levelname} {byclient} {creator} {havebeenreviewed} `{servername}` !",embed=embed2)
												except discord.errors.Forbidden:
													pass
												await msg.delete()
												
												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												msg101 = await channelmessageid.fetch_message(int(messages))

												try:
													await msg101.delete()
												except:
													pass
												
												embed3 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed3.add_field(name=f'`{level}` (**{levelname}** {byclient2} **{creator}**) {successreviewed}', value='\u200b')
												await message.channel.send(embed=embed3)
												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s", (level, ))
												conn.commit()

												cursor.execute(f"SELECT levelreviewedcount FROM users WHERE userid = {jaj}")
												counted = cursor.fetchone()[0]
												counted = counted + 1
												cursor.execute(f'UPDATE users SET levelreviewedcount = {counted} WHERE userid = {jaj}')
												conn.commit()
												if counted >= 1:
													cursor.execute(f'SELECT reviewachievement1 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement1 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement1(author)
														embed5 = reviewachievement1(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 5:
													cursor.execute(f'SELECT reviewachievement5 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement5 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement5(author)
														embed5 = reviewachievement5(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 10:
													cursor.execute(f'SELECT reviewachievement10 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement10 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement10(author)
														embed5 = reviewachievement10(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 50:
													cursor.execute(f'SELECT reviewachievement50 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement50 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement50(author)
														embed5 = reviewachievement50(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 100:
													cursor.execute(f'SELECT reviewachievement100 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement100 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement100(author)
														embed5 = reviewachievement100(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass

												cursor.execute(f"SELECT levelreviewapprovedcount FROM users WHERE userid = {user1}")
												counted2 = cursor.fetchone()[0]
												counted2 += 1
												cursor.execute(f'UPDATE users SET levelreviewapprovedcount = {counted2} WHERE userid = {user1}')
												conn.commit()
												if counted2 >= 1:
													cursor.execute(f'SELECT reviewapprovedachievement1 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement1 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement1(user1)
														embed5 = reviewapprovedachievement1(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 5:
													cursor.execute(f'SELECT reviewapprovedachievement5 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement5 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement5(user1)
														embed5 = reviewapprovedachievement5(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 10:
													cursor.execute(f'SELECT reviewapprovedachievement10 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement10 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement10(user1)
														embed5 = reviewapprovedachievement10(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 50:
													cursor.execute(f'SELECT reviewapprovedachievement50 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement50 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement50(user1)
														embed5 = reviewapprovedachievement50(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 100:
													cursor.execute(f'SELECT reviewapprovedachievement100 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement100 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement100(user1)
														embed5 = reviewapprovedachievement100(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												return
										else:
											await msg.delete()
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorcheckedreviewchannel}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
									else:
										jojo = cursor.execute(f"SELECT CheckedReviewChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
										try:
											checkedreviewchannel = cursor.fetchone()[0]
										except TypeError:
											checkedreviewchannel = None
										if checkedreviewchannel is not None:
											channel2 = client.get_channel(int(checkedreviewchannel))
											pogya = cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmod = cursor.fetchone()[0]
											except TypeError:
												gdmod = None
											if gdmod is not None:
												embed2 = discord.Embed(title=f'{leveltitle} {levelname} {byserver} {creator} (`{level}`) {reviewed} <:downloads:472907713727430658>', description=f"<:success:472908961176092702> - __{levelapprovedserver}__", color=0x00ff00)
												
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												embed2.set_thumbnail(url=f"{ratingemote}")
												if int(objectplus) >= 40000:
													embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed2.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed2.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed2.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												embed2.set_footer(text=f"{reviewedby} {message.author}")
												await channel2.send(f"<@{user1}>",embed=embed2)
												cursor.execute(f"UPDATE levels SET reviewed = 'yes' WHERE levelid = %s AND server = %s", (level, serverid))
												channel = await username.create_dm()

												cursor.execute(f"SELECT language FROM users WHERE userid = %s", (user1, ))
												try:
													language_author = cursor.fetchone()[0]
												except TypeError:
													language_author = language_default
												language22 = language
												translate2_messages = open(f"language/client/reqreview/{language22}.txt").read().splitlines()

												yourlevel = translate2_messages[12]
												byclient = translate2_messages[13]
												havebeenreviewed = translate2_messages[14]

												try:
													await channel.send(f"{yourlevel} {levelname} {byclient} {creator} {havebeenreviewed} `{servername}` !",embed=embed2)
												except discord.errors.Forbidden:
													pass
													
												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												msg101 = await channelmessageid.fetch_message(int(messages))

												try:
													await msg101.delete()
												except:
													pass
												
												await msg.delete()
												embed3 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed3.add_field(name=f'`{level}` (**{levelname}** {byclient2} **{creator}**) {successreviewed}', value='\u200b')
												await message.channel.send(embed=embed3)
												pognya = cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												gdmodchannel123 = cursor.fetchone()[0]
												channel3 = client.get_channel(int(gdmodchannel123))
												embed4 = discord.Embed(title=f'{gdmodlevelapproved}', color=0x00ff00)
												embed4.add_field(name=f'`{level}` (**{levelname}** {byserver} **{creator}**)', value='\u200b')

												cursor.execute(f"SELECT video FROM levels WHERE server = {serverid} AND levelid = {level}")
												videotype = cursor.fetchone()[0]
												if videotype is not None:
													embed4.add_field(name=f'\nVideo :', value=f"{videotype}", inline=False)
												
												pognyanya = cursor.execute(f"SELECT userid FROM GDmoderators WHERE serverid = {serverid} LIMIT 1")
												gdmodchannel1234 = cursor.fetchone()[0]
												msgmod = await channel3.send(f"<@{gdmodchannel1234}>",embed=embed4)
												msgmod2 = getattr(msgmod,"id")
												
												cursor.execute(f"UPDATE levels SET messageid = {msgmod2} WHERE server = {serverid} AND levelid = {level}")
												conn.commit()

												cursor.execute(f"SELECT levelreviewedcount FROM users WHERE userid = {jaj}")
												counted = cursor.fetchone()[0]
												counted = counted + 1
												cursor.execute(f'UPDATE users SET levelreviewedcount = {counted} WHERE userid = {jaj}')
												conn.commit()
												if counted >= 1:
													cursor.execute(f'SELECT reviewachievement1 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement1 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement1(author)
														embed5 = reviewachievement1(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 5:
													cursor.execute(f'SELECT reviewachievement5 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement5 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement5(author)
														embed5 = reviewachievement5(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 10:
													cursor.execute(f'SELECT reviewachievement10 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement10 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement10(author)
														embed5 = reviewachievement10(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 50:
													cursor.execute(f'SELECT reviewachievement50 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement50 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement50(author)
														embed5 = reviewachievement50(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 100:
													cursor.execute(f'SELECT reviewachievement100 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement100 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement100(author)
														embed5 = reviewachievement100(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass

												cursor.execute(f"SELECT levelreviewapprovedcount FROM users WHERE userid = {user1}")
												counted2 = cursor.fetchone()[0]
												counted2 += 1
												cursor.execute(f'UPDATE users SET levelreviewapprovedcount = {counted2} WHERE userid = {user1}')
												conn.commit()
												if counted2 >= 1:
													cursor.execute(f'SELECT reviewapprovedachievement1 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement1 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement1(user1)
														embed5 = reviewapprovedachievement1(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 5:
													cursor.execute(f'SELECT reviewapprovedachievement5 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement5 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement5(user1)
														embed5 = reviewapprovedachievement5(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 10:
													cursor.execute(f'SELECT reviewapprovedachievement10 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement10 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement10(user1)
														embed5 = reviewapprovedachievement10(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 50:
													cursor.execute(f'SELECT reviewapprovedachievement50 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement50 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement50(user1)
														embed5 = reviewapprovedachievement50(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 100:
													cursor.execute(f'SELECT reviewapprovedachievement100 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement100 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement100(user1)
														embed5 = reviewapprovedachievement100(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												return
											else:
												embed2 = discord.Embed(title=f'{leveltitle} {levelname} {byserver} {creator} (`{level}`) {reviewed} <:downloads:472907713727430658>', description=f"<:success:472908961176092702> - __{levelapprovedserver}__", color=0x00ff00)
												
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												embed2.set_thumbnail(url=f"{ratingemote}")
												if int(objectplus) >= 40000:
													embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed2.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed2.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed2.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												embed2.set_footer(text=f"{reviewedby} {message.author}")
												await channel2.send(f"<@{user1}>",embed=embed2)
												channel = await username.create_dm()

												cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
												try:
													language_author = cursor.fetchone()[0]
												except TypeError:
													language_author = language_default
												language22 = language
												translate2_messages = open(f"language/client/reqreview/{language22}.txt").read().splitlines()

												yourlevel = translate2_messages[12]
												byclient = translate2_messages[13]
												havebeenreviewed = translate2_messages[14]

												try:
													await channel.send(f"{yourlevel} {levelname} {byclient} {creator} {havebeenreviewed} `{servername}` !",embed=embed2)
												except discord.errors.Forbidden:
													pass
													
												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												msg101 = await channelmessageid.fetch_message(int(messages))

												try:
													await msg101.delete()
												except:
													pass
												
												await msg.delete()
												embed3 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed3.add_field(name=f'`{level}` (**{levelname}** {byclient2} **{creator}**) {successreviewed}', value='\u200b')
												await message.channel.send(embed=embed3)
												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s", (level, ))
												conn.commit()

												cursor.execute(f"SELECT levelreviewedcount FROM users WHERE userid = {jaj}")
												counted = cursor.fetchone()[0]
												counted = counted + 1
												cursor.execute(f'UPDATE users SET levelreviewedcount = {counted} WHERE userid = {jaj}')
												conn.commit()
												if counted >= 1:
													cursor.execute(f'SELECT reviewachievement1 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement1 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement1(author)
														embed5 = reviewachievement1(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 5:
													cursor.execute(f'SELECT reviewachievement5 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement5 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement5(author)
														embed5 = reviewachievement5(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 10:
													cursor.execute(f'SELECT reviewachievement10 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement10 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement10(author)
														embed5 = reviewachievement10(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 50:
													cursor.execute(f'SELECT reviewachievement50 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement50 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement50(author)
														embed5 = reviewachievement50(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted >= 100:
													cursor.execute(f'SELECT reviewachievement100 FROM users WHERE userid = {jaj}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewachievement100 = "yes" WHERE userid = {jaj}')
														conn.commit()
														reviewachievement100(author)
														embed5 = reviewachievement100(author)
														username = await client.fetch_user(int(jaj))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass

												cursor.execute(f"SELECT levelreviewapprovedcount FROM users WHERE userid = {user1}")
												counted2 = cursor.fetchone()[0]
												counted2 += 1
												cursor.execute(f'UPDATE users SET levelreviewapprovedcount = {counted2} WHERE userid = {user1}')
												conn.commit()
												if counted2 >= 1:
													cursor.execute(f'SELECT reviewapprovedachievement1 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement1 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement1(user1)
														embed5 = reviewapprovedachievement1(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 5:
													cursor.execute(f'SELECT reviewapprovedachievement5 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement5 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement5(user1)
														embed5 = reviewapprovedachievement5(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 10:
													cursor.execute(f'SELECT reviewapprovedachievement10 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement10 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement10(user1)
														embed5 = reviewapprovedachievement10(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 50:
													cursor.execute(f'SELECT reviewapprovedachievement50 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement50 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement50(user1)
														embed5 = reviewapprovedachievement50(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												if counted2 >= 100:
													cursor.execute(f'SELECT reviewapprovedachievement100 FROM users WHERE userid = {user1}')
													yesvalue = cursor.fetchone()[0]
													if yesvalue == "yes":
														pass
													elif yesvalue == "no":
														cursor.execute(f'UPDATE users SET reviewapprovedachievement100 = "yes" WHERE userid = {user1}')
														conn.commit()
														reviewapprovedachievement100(user1)
														embed5 = reviewapprovedachievement100(user1)
														username = await client.fetch_user(int(user1))
														channel = await username.create_dm()
														try:
															await channel.send(embed=embed5)
														except discord.errors.Forbidden:
															pass
													else:
														pass
												return
										else:
											await msg.delete()
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorcheckedreviewchannel}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
								elif validation == "no":
									if feedback:
										sentence = ' '.join(feedback)
										jojo = cursor.execute(f"SELECT CheckedReviewChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
										try:
											checkedreviewchannel = cursor.fetchone()[0]
										except TypeError:
											checkedreviewchannel = None
										if checkedreviewchannel is not None:
											channel2 = client.get_channel(int(checkedreviewchannel))
											embed2 = discord.Embed(title=f'{leveltitle} {levelname} {byserver} {creator} (`{level}`) {reviewed} <:downloads:472907713727430658>', description=f"<:error:472907618386575370> - {sentence}", color=0xff0000)
											
											#reqsearch(level)
											stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
											description += '=' * (-len(description) % 4)
											base64_bytes = description.encode('ascii')
											
											message_bytes = base64.urlsafe_b64decode(base64_bytes)
											descbase64 = message_bytes.decode('ascii')

											embed2.set_thumbnail(url=f"{ratingemote}")
											if int(objectplus) >= 40000:
												embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
											elif int(objectplus) <= 39999:
												embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

											if int(coins) == 0:
												coinsvalue = f"{none}"
											elif int(coins) == 1:
												coinsvalue = "<:user_coin_unverified:472908993832943631>"
											elif int(coins) == 2:
												coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
											elif int(coins) == 3:
												coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

											try:
												if int(verifiedcoins) == 1:
													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin:472908993711308800>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
											except ValueError:
												pass

											embed2.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

											#reqsearch2(level)
											try:
												songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
											except ValueError:
												songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

											songlink2 = unquote(f"{songlink}")
											try:
												officialsong2 = int(officialsong)
											except UnboundLocalError:
												embed2.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
											else:
												embed2.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
											embed2.set_footer(text=f"{reviewedby} {message.author}")
											await channel2.send(f"<@{user1}>",embed=embed2)
											channel = await username.create_dm()

											cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
											try:
												language_author = cursor.fetchone()[0]
											except TypeError:
												language_author = language_default
											language22 = language
											translate2_messages = open(f"language/client/reqreview/{language22}.txt").read().splitlines()

											yourlevel = translate2_messages[12]
											byclient = translate2_messages[13]
											havebeenreviewed = translate2_messages[14]

											try:
												await channel.send(f"{yourlevel} {levelname} {byclient} {creator} {havebeenreviewed} `{servername}` !",embed=embed2)
											except discord.errors.Forbidden:
												pass
												
											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											msg101 = await channelmessageid.fetch_message(int(messages))

											try:
												await msg101.delete()
											except:
												pass
											
											await msg.delete()
											embed3 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed3.add_field(name=f'`{level}` (**{levelname}** {byclient2} **{creator}**) {successreviewed}', value='\u200b')
											await message.channel.send(embed=embed3)
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s AND server = %s", (level, serverid))
											conn.commit()

											cursor.execute(f"SELECT levelreviewedcount FROM users WHERE userid = {jaj}")
											counted = cursor.fetchone()[0]
											counted = counted + 1
											cursor.execute(f'UPDATE users SET levelreviewedcount = {counted} WHERE userid = {jaj}')
											conn.commit()
											if counted >= 1:
												cursor.execute(f'SELECT reviewachievement1 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewachievement1 = "yes" WHERE userid = {jaj}')
													conn.commit()
													reviewachievement1(author)
													embed5 = reviewachievement1(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted >= 5:
												cursor.execute(f'SELECT reviewachievement5 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewachievement5 = "yes" WHERE userid = {jaj}')
													conn.commit()
													reviewachievement5(author)
													embed5 = reviewachievement5(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted >= 10:
												cursor.execute(f'SELECT reviewachievement10 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewachievement10 = "yes" WHERE userid = {jaj}')
													conn.commit()
													reviewachievement10(author)
													embed5 = reviewachievement10(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted >= 50:
												cursor.execute(f'SELECT reviewachievement50 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewachievement50 = "yes" WHERE userid = {jaj}')
													conn.commit()
													reviewachievement50(author)
													embed5 = reviewachievement50(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted >= 100:
												cursor.execute(f'SELECT reviewachievement100 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewachievement100 = "yes" WHERE userid = {jaj}')
													conn.commit()
													reviewachievement100(author)
													embed5 = reviewachievement100(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass

											cursor.execute(f"SELECT levelreviewunapprovedcount FROM users WHERE userid = {user1}")
											counted2 = cursor.fetchone()[0]
											counted2 += 1
											cursor.execute(f'UPDATE users SET levelreviewunapprovedcount = {counted2} WHERE userid = {user1}')
											conn.commit()
											if counted2 >= 1:
												cursor.execute(f'SELECT reviewunapprovedachievement1 FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewunapprovedachievement1 = "yes" WHERE userid = {user1}')
													conn.commit()
													reviewunapprovedachievement1(user1)
													embed5 = reviewunapprovedachievement1(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted2 >= 5:
												cursor.execute(f'SELECT reviewunapprovedachievement5 FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewunapprovedachievement5 = "yes" WHERE userid = {user1}')
													conn.commit()
													reviewunapprovedachievement5(user1)
													embed5 = reviewunapprovedachievement5(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted2 >= 10:
												cursor.execute(f'SELECT reviewunapprovedachievement10 FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewunapprovedachievement10 = "yes" WHERE userid = {user1}')
													conn.commit()
													reviewunapprovedachievement10(user1)
													embed5 = reviewunapprovedachievement10(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted2 >= 50:
												cursor.execute(f'SELECT reviewunapprovedachievement50 FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewunapprovedachievement50 = "yes" WHERE userid = {user1}')
													conn.commit()
													reviewunapprovedachievement50(user1)
													embed5 = reviewunapprovedachievement50(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted2 >= 100:
												cursor.execute(f'SELECT reviewunapprovedachievement100 FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewunapprovedachievement100 = "yes" WHERE userid = {user1}')
													conn.commit()
													reviewunapprovedachievement100(user1)
													embed5 = reviewunapprovedachievement100(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											return
										else:
											await msg.delete()
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorcheckedreviewchannel}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
									else:
										jojo = cursor.execute(f"SELECT CheckedReviewChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
										try:
											checkedreviewchannel = cursor.fetchone()[0]
										except TypeError:
											checkedreviewchannel = None
										if checkedreviewchannel is not None:
											channel2 = client.get_channel(int(checkedreviewchannel))
											embed2 = discord.Embed(title=f'{leveltitle} {levelname} {byserver} {creator} (`{level}`) {reviewed} <:downloads:472907713727430658>', description=f"<:error:472907618386575370> - __{levelunapprovedserver}__", color=0xff0000)
											
											#reqsearch(level)
											stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
											description += '=' * (-len(description) % 4)
											base64_bytes = description.encode('ascii')
											
											message_bytes = base64.urlsafe_b64decode(base64_bytes)
											descbase64 = message_bytes.decode('ascii')

											embed2.set_thumbnail(url=f"{ratingemote}")
											if int(objectplus) >= 40000:
												embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
											elif int(objectplus) <= 39999:
												embed2.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

											if int(coins) == 0:
												coinsvalue = f"{none}"
											elif int(coins) == 1:
												coinsvalue = "<:user_coin_unverified:472908993832943631>"
											elif int(coins) == 2:
												coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
											elif int(coins) == 3:
												coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

											try:
												if int(verifiedcoins) == 1:
													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin:472908993711308800>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
											except ValueError:
												pass

											embed2.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

											#reqsearch2(level)
											try:
												songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
											except ValueError:
												songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

											songlink2 = unquote(f"{songlink}")
											try:
												officialsong2 = int(officialsong)
											except UnboundLocalError:
												embed2.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
											else:
												embed2.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
											embed2.set_footer(text=f"{reviewedby} {message.author}")
											await channel2.send(f"<@{user1}>",embed=embed2)
											channel = await username.create_dm()

											cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
											try:
												language_author = cursor.fetchone()[0]
											except TypeError:
												language_author = language_default
											language22 = language
											translate2_messages = open(f"language/client/reqreview/{language22}.txt").read().splitlines()

											yourlevel = translate2_messages[12]
											byclient = translate2_messages[13]
											havebeenreviewed = translate2_messages[14]

											try:
												await channel.send(f"{yourlevel} {levelname} {byclient} {creator} {havebeenreviewed} `{servername}` !",embed=embed2)
											except discord.errors.Forbidden:
												pass
												
											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											msg101 = await channelmessageid.fetch_message(int(messages))

											try:
												await msg101.delete()
											except:
												pass
											
											await msg.delete()
											embed3 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed3.add_field(name=f'`{level}` (**{levelname}** {byclient2} **{creator}**) {successreviewed}', value='\u200b')
											await message.channel.send(embed=embed3)
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s AND server = %s", (level, serverid))
											conn.commit()

											cursor.execute(f"SELECT levelreviewedcount FROM users WHERE userid = {jaj}")
											counted = cursor.fetchone()[0]
											counted = counted + 1
											cursor.execute(f'UPDATE users SET levelreviewedcount = {counted} WHERE userid = {jaj}')
											conn.commit()
											if counted >= 1:
												cursor.execute(f'SELECT reviewachievement1 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewachievement1 = "yes" WHERE userid = {jaj}')
													conn.commit()
													reviewachievement1(author)
													embed5 = reviewachievement1(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted >= 5:
												cursor.execute(f'SELECT reviewachievement5 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewachievement5 = "yes" WHERE userid = {jaj}')
													conn.commit()
													reviewachievement5(author)
													embed5 = reviewachievement5(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted >= 10:
												cursor.execute(f'SELECT reviewachievement10 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewachievement10 = "yes" WHERE userid = {jaj}')
													conn.commit()
													reviewachievement10(author)
													embed5 = reviewachievement10(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted >= 50:
												cursor.execute(f'SELECT reviewachievement50 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewachievement50 = "yes" WHERE userid = {jaj}')
													conn.commit()
													reviewachievement50(author)
													embed5 = reviewachievement50(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted >= 100:
												cursor.execute(f'SELECT reviewachievement100 FROM users WHERE userid = {jaj}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewachievement100 = "yes" WHERE userid = {jaj}')
													conn.commit()
													reviewachievement100(author)
													embed5 = reviewachievement100(author)
													username = await client.fetch_user(int(jaj))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass

											cursor.execute(f"SELECT levelreviewunapprovedcount FROM users WHERE userid = {user1}")
											counted2 = cursor.fetchone()[0]
											counted2 += 1
											cursor.execute(f'UPDATE users SET levelreviewunapprovedcount = {counted2} WHERE userid = {user1}')
											conn.commit()
											if counted2 >= 1:
												cursor.execute(f'SELECT reviewunapprovedachievement1 FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewunapprovedachievement1 = "yes" WHERE userid = {user1}')
													conn.commit()
													reviewunapprovedachievement1(user1)
													embed5 = reviewunapprovedachievement1(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted2 >= 5:
												cursor.execute(f'SELECT reviewunapprovedachievement5 FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewunapprovedachievement5 = "yes" WHERE userid = {user1}')
													conn.commit()
													reviewunapprovedachievement5(user1)
													embed5 = reviewunapprovedachievement5(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted2 >= 10:
												cursor.execute(f'SELECT reviewunapprovedachievement10 FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewunapprovedachievement10 = "yes" WHERE userid = {user1}')
													conn.commit()
													reviewunapprovedachievement10(user1)
													embed5 = reviewunapprovedachievement10(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted2 >= 50:
												cursor.execute(f'SELECT reviewunapprovedachievement50 FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewunapprovedachievement50 = "yes" WHERE userid = {user1}')
													conn.commit()
													reviewunapprovedachievement50(user1)
													embed5 = reviewunapprovedachievement50(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											if counted2 >= 100:
												cursor.execute(f'SELECT reviewunapprovedachievement100 FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET reviewunapprovedachievement100 = "yes" WHERE userid = {user1}')
													conn.commit()
													reviewunapprovedachievement100(user1)
													embed5 = reviewunapprovedachievement100(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												else:
													pass
											return
										else:
											await msg.delete()
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorcheckedreviewchannel}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
								else:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									embed.add_field(name=f'{errormessage}', value=f"{errorsyntax}")
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
							else:
								await msg.delete()
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorban}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
						else:
							await msg.delete()
							embed = discord.Embed(title="", color=0xff0000)
						#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
							embed.add_field(name=f'{errormessage}', value=f"{errorrequiredrole}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
					maybe_number = cursor.fetchone()
				else:
					await msg.delete()
					embed = discord.Embed(title="", color=0xff0000)
					#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
					embed.add_field(name=f'{errormessage}', value=f'{errornotfound1} `{level}` {errornotfound2}')
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

		if msg.startswith("send"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqsend"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				args = [x for ar in args for x in ar.split('\n')]

				author = message.author.id
				serverid = message.guild.id
				
				try:
					level = args[1]
				except IndexError as error:
					level = 0
				try:
					validation = args[2]
				except IndexError as error:
					validation = None
				try:
					star = args[3]
				except IndexError as error:
					star = None
				try:
					demon = args[4]
				except IndexError as error:
					demon = None

				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
					
				cursor.execute(f"SELECT language FROM setup WHERE serverid = {serverid}")
				try:
					languageserver = cursor.fetchone()[0]
				except TypeError:
					languageserver = language_default
				language2 = language
				translate_messages = open(f"language/client/reqsend/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorqueue1 = translate_messages[4]
				errorqueue2 = translate_messages[5]
				errorsyntax = translate_messages[6]
				errorrate = translate_messages[7]
				errorban = translate_messages[8]
				errorblacklist = translate_messages[9]
				errorpermission = translate_messages[10]

				successtitle = translate_messages[12]
				thelevel = translate_messages[13]
				by = translate_messages[14]
				successsend = translate_messages[15]
				
				translate_messages_search = open(f"language/server/reqsearch/{languageserver}.txt").read().splitlines()

				searchresult = translate_messages_search[3]
				desc = translate_messages_search[5]
				none = translate_messages_search[6]
				coinstitle = translate_messages_search[7]
				sizetitle = translate_messages_search[8]
				newgroundsplay = translate_messages_search[9]
				downloadsong = translate_messages_search[10]
				detailledsong = translate_messages_search[11]
				idleveltitle = translate_messages_search[12]
				levelversiontitle = translate_messages_search[13]
				minimumgdver = translate_messages_search[14]
				objectcount = translate_messages_search[15]
				lagtitleobject = translate_messages_search[16]
				youtubelink = translate_messages_search[17]
				officialsongtitle = translate_messages_search[18]
				
				translate_messages_send = open(f"language/server/reqsend/{languageserver}.txt").read().splitlines()
				
				sendfor = translate_messages_send[0]

				data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={level}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
				result = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)
				pog = cursor.execute(f"SELECT userid FROM GDmoderators WHERE userid = {author} LIMIT 1")
				gdmod = cursor.fetchone()
				if gdmod is not None:
					result = result.split(":")
					levelname = result[3]
					creator = convertinfo("u","n",result[7])
					if message.author.guild_permissions.administrator:
						poggery = cursor.execute(f"SELECT isBlacklist FROM reports WHERE levelid = %s", (level, ))
						maybe_number2 = cursor.fetchone()
						if maybe_number2 is None:
							poggare = cursor.execute(f"SELECT userid FROM banned WHERE userid = {author}")
							maybe_number3 = cursor.fetchone()
							if maybe_number3 is None:
								pogaga = cursor.execute(f"SELECT levelid FROM levels WHERE server = {serverid} AND levelid = %s LIMIT 1", (level, ))
								try:
									maybe_number4 = cursor.fetchone()[0]
								except TypeError:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
									embed.add_field(name=f'{errormessage}', value=f'{errorqueue1} `{level}` {errorqueue2}')
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
								cursor.execute(f"SELECT server FROM levels WHERE server = {serverid} AND levelid = %s LIMIT 1", (level, ))
								try:
									maybe_number12345 = cursor.fetchone()[0]
								except TypeError:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
									embed.add_field(name=f'{errormessage}', value=f'{errorqueue1} `{level}` {errorqueue2}')
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
								if str(maybe_number4) == str(level):
									#reqsearch(level)
									stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
									
									embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
									if validation == "star":
										nyaya = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
										user1 = cursor.fetchone()[0]
										username = await client.fetch_user(int(user1))

										cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
										try:
											language_requester = cursor.fetchone()[0]
										except TypeError:
											language_requester = language_default
										language2_requester = language_requester
										translate_messages_requester = open(f"language/requester/reqsend/{language2}.txt").read().splitlines()

										successtitlerequester = translate_messages_requester[0]
										thelevelyourequested = translate_messages_requester[1]
										byrequester = translate_messages_requester[2]
										sendtorobtop = translate_messages_requester[3]
										fortext = translate_messages_requester[4]

										if star == "1":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907799987486768.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **AUTO 1<:starrate:718204629858517003> RATE**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **AUTO 1<:starrate:718204629858517003> RATE** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass

											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = {serverid} AND server = {serverid}", (level, ))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
												
												embed13.add_field(name=f"{sendfor} **AUTO 1<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472907799987486768.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "2":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908189059383296.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **EASY 2<:starrate:718204629858517003> RATE**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **EASY 2<:starrate:718204629858517003> RATE** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass

											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} EASY 2<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908189059383296.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "3":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908581319213056.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **NORMAL 3<:starrate:718204629858517003> RATE**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **NORMAL 3<:starrate:718204629858517003> RATE** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass
											
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} NORMAL 3<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908581319213056.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "4":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908253408395296.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **HARD 4<:starrate:718204629858517003> RATE**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **HARD 4<:starrate:718204629858517003> RATE** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass
											
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} HARD 4<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908253408395296.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "5":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908253408395296.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **HARD 5<:starrate:718204629858517003> RATE**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **HARD 5<:starrate:718204629858517003> RATE** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass

											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} HARD 5<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908253408395296.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "6":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908316301852683.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **HARDER 6<:starrate:718204629858517003> RATE**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **HARDER 6<:starrate:718204629858517003> RATE** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass

											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} HARDER 6<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908316301852683.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "7":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908316301852683.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **HARDER 7<:starrate:718204629858517003> RATE**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **HARDER 7<:starrate:718204629858517003> RATE** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass
											
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} HARDER 7<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908316301852683.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "8":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908421209784320.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **INSANE 8<:starrate:718204629858517003> RATE**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **INSANE 8<:starrate:718204629858517003> RATE** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass
											
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} INSANE 8<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908421209784320.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "9":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908421209784320.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **INSANE 9<:starrate:718204629858517003> RATE**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **INSANE 9<:starrate:718204629858517003> RATE** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass
											
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} INSANE 9<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908421209784320.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "10":
											if demon == "1":
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907861102559262.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **EASY DEMON 10<:starrate:718204629858517003> RATE**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **EASY DEMON 10<:starrate:718204629858517003> RATE** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass
												
												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} EASY DEMON 10<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472907861102559262.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
											elif demon == "2":
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908111053586433.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **MEDIUM DEMON 10<:starrate:718204629858517003> RATE**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **MEDIUM DEMON 10<:starrate:718204629858517003> RATE** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass

												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} MEDIUM DEMON 10<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908111053586433.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
											elif demon == "3":
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907978094411776.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **HARD DEMON 10<:starrate:718204629858517003> RATE**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **HARD DEMON 10<:starrate:718204629858517003> RATE** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass

												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} HARD DEMON 10<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472907978094411776.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
											elif demon == "4":
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908041960947712.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **INSANE DEMON 10<:starrate:718204629858517003> RATE**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **INSANE DEMON 10<:starrate:718204629858517003> RATE** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass
												
												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} INSANE DEMON 10<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908041960947712.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
											elif demon == "5":
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907914110304267.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **EXTREME DEMON 10<:starrate:718204629858517003> RATE**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **EXTREME DEMON 10<:starrate:718204629858517003> RATE** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass

												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} EXTREME DEMON 10<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472907914110304267.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
											else:
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907978094411776.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **DEMON 10<:starrate:718204629858517003> RATE**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **DEMON 10<:starrate:718204629858517003> RATE** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass

												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} DEMON 10<:starrate:718204629858517003> RATE** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472907978094411776.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
										else:
											await msg.delete()
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorsyntax}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
									elif validation == "featured":
										nyaya = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
										user1 = cursor.fetchone()[0]
										username = await client.fetch_user(int(user1))

										cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
										try:
											language_requester = cursor.fetchone()[0]
										except TypeError:
											language_requester = language_default
										language2_requester = language_requester
										translate_messages_requester = open(f"language/requester/reqsend/{language2}.txt").read().splitlines()

										successtitlerequester = translate_messages_requester[0]
										thelevelyourequested = translate_messages_requester[1]
										byrequester = translate_messages_requester[2]
										sendtorobtop = translate_messages_requester[3]
										fortext = translate_messages_requester[4]

										if star == "1":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907828185792532.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **AUTO 1<:starrate:718204629858517003> FEATURED**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **AUTO 1<:starrate:718204629858517003> FEATURED** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass

											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} AUTO 1<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472907828185792532.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "2":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908214766141471.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **EASY 2<:starrate:718204629858517003> FEATURED**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **EASY 2<:starrate:718204629858517003> FEATURED** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass

											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} EASY 2<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908214766141471.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "3":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908602613563392.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **NORMAL 3<:starrate:718204629858517003> FEATURED**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **NORMAL 3<:starrate:718204629858517003> FEATURED** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass
											
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} NORMAL 3<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908602613563392.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "4":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908272781754369.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **HARD 4<:starrate:718204629858517003> FEATURED**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **HARD 4<:starrate:718204629858517003> FEATURED** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass
											
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} HARD 4<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908272781754369.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "5":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908272781754369.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **HARD 5<:starrate:718204629858517003> FEATURED**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **HARD 5<:starrate:718204629858517003> FEATURED** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass

											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} HARD 5<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908272781754369.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "6":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908356928143370.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **HARDER 6<:starrate:718204629858517003> FEATURED**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **HARDER 6<:starrate:718204629858517003> FEATURED** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass

											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} HARDER 6<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908356928143370.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "7":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908356928143370.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **HARDER 7<:starrate:718204629858517003> FEATURED**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **HARDER 7<:starrate:718204629858517003> FEATURED** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass
											
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} HARDER 7<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908356928143370.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "8":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908439958323211.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **INSANE 8<:starrate:718204629858517003> FEATURED**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **INSANE 8<:starrate:718204629858517003> FEATURED** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass
											
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} INSANE 8<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908439958323211.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "9":
											await msg.delete()
											papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
											gdmodname = cursor.fetchone()[0]
											embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
											embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908439958323211.png?v=1")
											embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **INSANE 9<:starrate:718204629858517003> FEATURED**', value='\u200b')
											if message.attachments:
												fileimage = message.attachments[0]
												imageurl = fileimage.url
												for ext in pic_ext:
													if imageurl.endswith(ext):
														embed3.set_image(url=f"{imageurl}")
											channel = await username.create_dm()
											try:
												await channel.send(embed=embed3)
											except discord.errors.Forbidden:
												pass
											nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
											user1 = cursor.fetchone()[0]
											username = await client.fetch_user(int(user1))
											embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
											embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **INSANE 9<:starrate:718204629858517003> FEATURED** !', value='\u200b')
											await message.channel.send(embed=embed4)

											cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))

											cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
											messages = cursor.fetchone()[0]
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													pass
											
											delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
											conn.commit()
											
											cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
											try:
												gdmodcheckedchannel = cursor.fetchone()[0]
											except TypeError:
												gdmodcheckedchannel = None
											if gdmodcheckedchannel is not None:
												channelmod = client.get_channel(int(gdmodcheckedchannel))
														
												#reqsearch(level)
												stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
												
												embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
												embed13.add_field(name=f"{sendfor} INSANE 9<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
												embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908439958323211.png?v=1")
		
												description += '=' * (-len(description) % 4)
												base64_bytes = description.encode('ascii')
												
												message_bytes = base64.urlsafe_b64decode(base64_bytes)
												descbase64 = message_bytes.decode('ascii')

												if int(objectplus) >= 40000:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
												elif int(objectplus) <= 39999:
													embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

												if int(coins) == 0:
													coinsvalue = f"{none}"
												elif int(coins) == 1:
													coinsvalue = "<:user_coin_unverified:472908993832943631>"
												elif int(coins) == 2:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
												elif int(coins) == 3:
													coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

												try:
													if int(verifiedcoins) == 1:
														if int(coins) == 0:
															coinsvalue = f"{none}"
														elif int(coins) == 1:
															coinsvalue = "<:user_coin:472908993711308800>"
														elif int(coins) == 2:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
														elif int(coins) == 3:
															coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
												except ValueError:
													pass

												embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

												#reqsearch2(level)
												try:
													songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
												except ValueError:
													songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

												songlink2 = unquote(f"{songlink}")
												try:
													officialsong2 = int(officialsong)
												except UnboundLocalError:
													embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
												else:
													embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
												
												await channelmod.send(f"<@{user1}>",embed=embed13)
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
															embed14.set_image(url=f"{imageurl}")
															await channelmod.send(embed=embed14)

											cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
											yesvalue = cursor.fetchone()[0]
											if yesvalue == "yes":
												pass
											elif yesvalue == "no":
												cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
												conn.commit()
												levelsentbygdmod(user1)
												embed5 = levelsentbygdmod(user1)
												username = await client.fetch_user(int(user1))
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed5)
												except discord.errors.Forbidden:
													pass
											return
										elif star == "10":
											if demon == "1":
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907878790070273.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **EASY DEMON 10<:starrate:718204629858517003> FEATURED**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **EASY DEMON 10<:starrate:718204629858517003> FEATURED** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass
												
												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} EASY DEMON 10<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472907878790070273.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
											elif demon == "2":
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908128472793089.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **MEDIUM DEMON 10<:starrate:718204629858517003> FEATURED**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **MEDIUM DEMON 10<:starrate:718204629858517003> FEATURED** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass
												
												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} MEDIUM DEMON 10<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908128472793089.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
											elif demon == "3":
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907996901408778.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **HARD DEMON 10<:starrate:718204629858517003> FEATURED**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **HARD DEMON 10<:starrate:718204629858517003> FEATURED** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass
												
												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} HARD DEMON 10<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472907996901408778.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
											elif demon == "4":
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472908062269636640.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **INSANE DEMON 10<:starrate:718204629858517003> FEATURED**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **INSANE DEMON 10<:starrate:718204629858517003> FEATURED** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass
												
												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} INSANE DEMON 10<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472908062269636640.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
											elif demon == "5":
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907934633033738.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **EXTREME DEMON 10<:starrate:718204629858517003> FEATURED**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **EXTREME DEMON 10<:starrate:718204629858517003> FEATURED** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass
												
												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} INSANE DEMON 10<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472907934633033738.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
											else:
												await msg.delete()
												papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
												gdmodname = cursor.fetchone()[0]
												embed3 = discord.Embed(title=f'{successtitlerequester}', color=0x00ff00)
												embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907996901408778.png?v=1")
												embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {sendtorobtop} {gdmodname} {fortext} **DEMON 10<:starrate:718204629858517003> FEATURED**', value='\u200b')
												if message.attachments:
													fileimage = message.attachments[0]
													imageurl = fileimage.url
													for ext in pic_ext:
														if imageurl.endswith(ext):
															embed3.set_image(url=f"{imageurl}")
												channel = await username.create_dm()
												try:
													await channel.send(embed=embed3)
												except discord.errors.Forbidden:
													pass
												nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
												user1 = cursor.fetchone()[0]
												username = await client.fetch_user(int(user1))
												embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
												embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend} **DEMON 10<:starrate:718204629858517003> FEATURED** !', value='\u200b')
												await message.channel.send(embed=embed4)

												cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
												channelmessageid = cursor.fetchone()[0]
												channelmessageid = client.get_channel(int(channelmessageid))

												cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
												messages = cursor.fetchone()[0]
												try:
													msg101 = await channelmessageid.fetch_message(int(messages))
													await msg101.delete()
												except:
													cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
													channelmessageid = cursor.fetchone()[0]
													channelmessageid = client.get_channel(int(channelmessageid))
													try:
														msg101 = await channelmessageid.fetch_message(int(messages))
														await msg101.delete()
													except:
														pass
												
												delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = %s", (level, serverid))
												conn.commit()
												
												cursor.execute(f"SELECT GDModCheckedChannel FROM setup WHERE serverid = {serverid} LIMIT 1")
												try:
													gdmodcheckedchannel = cursor.fetchone()[0]
												except TypeError:
													gdmodcheckedchannel = None
												if gdmodcheckedchannel is not None:
													channelmod = client.get_channel(int(gdmodcheckedchannel))
															
													#reqsearch(level)
													stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
													
													embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {by} **{creator}**)', color=0x00ff00)
													embed13.add_field(name=f"{sendfor} DEMON 10<:starrate:718204629858517003> FEATURED** ! <:success:472908961176092702>", value="\u200b")
													embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/472907996901408778.png?v=1")
			
													description += '=' * (-len(description) % 4)
													base64_bytes = description.encode('ascii')
													
													message_bytes = base64.urlsafe_b64decode(base64_bytes)
													descbase64 = message_bytes.decode('ascii')

													if int(objectplus) >= 40000:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
													elif int(objectplus) <= 39999:
														embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {by} {creator}', value=f"{desc} {descbase64}", inline=False)

													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin_unverified:472908993832943631>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

													try:
														if int(verifiedcoins) == 1:
															if int(coins) == 0:
																coinsvalue = f"{none}"
															elif int(coins) == 1:
																coinsvalue = "<:user_coin:472908993711308800>"
															elif int(coins) == 2:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
															elif int(coins) == 3:
																coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													except ValueError:
														pass

													embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

													#reqsearch2(level)
													try:
														songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
													except ValueError:
														songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

													songlink2 = unquote(f"{songlink}")
													try:
														officialsong2 = int(officialsong)
													except UnboundLocalError:
														embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
													else:
														embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
													
													await channelmod.send(f"<@{user1}>",embed=embed13)
													if message.attachments:
														fileimage = message.attachments[0]
														imageurl = fileimage.url
														for ext in pic_ext:
															if imageurl.endswith(ext):
																embed14 = discord.Embed(title=f'Screenshot', color=0x00ff00)
																embed14.set_image(url=f"{imageurl}")
																await channelmod.send(embed=embed14)

												cursor.execute(f'SELECT levelsentbygdmod FROM users WHERE userid = {user1}')
												yesvalue = cursor.fetchone()[0]
												if yesvalue == "yes":
													pass
												elif yesvalue == "no":
													cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user1}')
													conn.commit()
													levelsentbygdmod(user1)
													embed5 = levelsentbygdmod(user1)
													username = await client.fetch_user(int(user1))
													channel = await username.create_dm()
													try:
														await channel.send(embed=embed5)
													except discord.errors.Forbidden:
														pass
												return
										else:
											await msg.delete()
											embed = discord.Embed(title="", color=0xff0000)
											embed.add_field(name=f'{errormessage}', value=f"{errorsyntax}")
											msg2 = await message.channel.send(embed=embed)
											time.sleep(5)
											await msg2.delete()
											return
									else:
										await msg.delete()
										embed = discord.Embed(title="", color=0xff0000)
										embed.add_field(name=f'{errormessage}', value=f"{errorrate}")
										msg2 = await message.channel.send(embed=embed)
										time.sleep(5)
										await msg2.delete()
										return
								else:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
									embed.add_field(name=f'{errormessage}', value=f'{errorqueue1} `{level}` {errorqueue2}')
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
							else:
								await msg.delete()
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorban}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
						else:
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title="", color=0xff0000)
							#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
							embed.add_field(name=f'{errormessage}', value=f'{errorblacklist}')
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
					else:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errorpermission}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
				else:
					await msg.delete()
					embed = discord.Embed(title="", color=0xff0000)
					#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
					embed.add_field(name=f'{errormessage}', value=f"{errorpermission}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

		if msg.startswith("notsend"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqnotsend"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				args = [x for ar in args for x in ar.split('\n')]

				author = message.author.id
				serverid = message.guild.id

				try:
					level = args[1]
				except IndexError as error:
					level = 0
				try:
					reason = args[2:]
				except IndexError as error:
					reason = None
				
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
					
				cursor.execute(f"SELECT language FROM setup WHERE serverid = {serverid}")
				try:
					languageserver = cursor.fetchone()[0]
				except TypeError:
					languageserver = language_default
				language2 = language
				translate_messages = open(f"language/client/reqnotsend/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorqueue1 = translate_messages[4]
				errorqueue2 = translate_messages[5]
				errorsyntax = translate_messages[6]
				errorrate = translate_messages[7]
				errorban = translate_messages[8]
				errorblacklist = translate_messages[9]
				errorpermission = translate_messages[10]

				successtitle = translate_messages[12]
				thelevel = translate_messages[13]
				by = translate_messages[14]
				successsend = translate_messages[15]

				translate_messages_server = open(f"language/server/reqnotsend/{languageserver}.txt").read().splitlines()

				byserver = translate_messages_server[0]
				notsendserver = translate_messages_server[1]
				reasonserver = translate_messages_server[2]
				
				translate_messages_search = open(f"language/server/reqsearch/{languageserver}.txt").read().splitlines()

				searchresult = translate_messages_search[3]
				desc = translate_messages_search[5]
				none = translate_messages_search[6]
				coinstitle = translate_messages_search[7]
				sizetitle = translate_messages_search[8]
				newgroundsplay = translate_messages_search[9]
				downloadsong = translate_messages_search[10]
				detailledsong = translate_messages_search[11]
				idleveltitle = translate_messages_search[12]
				levelversiontitle = translate_messages_search[13]
				minimumgdver = translate_messages_search[14]
				objectcount = translate_messages_search[15]
				lagtitleobject = translate_messages_search[16]
				youtubelink = translate_messages_search[17]
				officialsongtitle = translate_messages_search[18]

				data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={level}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
				result = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)
				pog = cursor.execute(f"SELECT userid FROM GDmoderators WHERE userid = {author} LIMIT 1")
				gdmod = cursor.fetchone()
				if gdmod is not None:
					result = result.split(":")
					levelname = result[3]
					creator = convertinfo("u","n",result[7])
					if message.author.guild_permissions.administrator:
						poggery = cursor.execute(f"SELECT isBlacklist FROM reports WHERE levelid = %s", (level, ))
						maybe_number2 = cursor.fetchone()
						if maybe_number2 is None:
							poggare = cursor.execute(f"SELECT userid FROM banned WHERE userid = {author}")
							maybe_number3 = cursor.fetchone()
							if maybe_number3 is None:
								pogaga = cursor.execute(f"SELECT levelid FROM levels WHERE server = {serverid} AND levelid = %s LIMIT 1", (level, ))
								try:
									maybe_number4 = cursor.fetchone()[0]
								except TypeError:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									embed.add_field(name=f'{errormessage}', value=f'{errorqueue1} `{level}` {errorqueue2}')
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
								cursor.execute(f"SELECT server FROM levels WHERE server = {serverid} AND levelid = %s LIMIT 1", (level, ))
								try:
									maybe_number12345 = cursor.fetchone()[0]
								except TypeError:
									await msg.delete()
									embed = discord.Embed(title="", color=0xff0000)
									embed.add_field(name=f'{errormessage}', value=f'{errorqueue1} `{level}` {errorqueue2}')
									msg2 = await message.channel.send(embed=embed)
									time.sleep(5)
									await msg2.delete()
									return
								if str(maybe_number4) == str(level):
									stars,objectplus,levelname,creator,ratingemote,stars,downloads,likes,likesemote,description,coins,verifiedcoins,lengthvalue,idlevel,version,gdversion,color = reqsearch(level)
									
									embed13 = discord.Embed(title=f'`{level}` (**{levelname}** {byserver} **{creator}**)', color=0xff0000)
									if reason is not None:
										nyaya = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
										user1 = cursor.fetchone()[0]
										username = await client.fetch_user(int(user1))

										cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
										try:
											language_requester = cursor.fetchone()[0]
										except TypeError:
											language_requester = language_default
										language2_requester = language_requester
										translate_messages_requester = open(f"language/requester/reqnotsend/{language2}.txt").read().splitlines()

										successtitlerequester = translate_messages_requester[0]
										thelevelyourequested = translate_messages_requester[1]
										byrequester = translate_messages_requester[2]
										notsendrequester = translate_messages_requester[3]
										reasonrequester = translate_messages_requester[4]

										await msg.delete()
										papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
										gdmodname = cursor.fetchone()[0]
										embed3 = discord.Embed(title=f'{successtitlerequester}', color=0xff0000)
										embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/693237079538270261.png?v=1")
										embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {notsendrequester} {gdmodname}.\n\n{reasonrequester} {reason}', value='\u200b')
										channel = await username.create_dm()
										try:
											await channel.send(embed=embed3)
										except discord.errors.Forbidden:
											pass
										
										nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
										user1 = cursor.fetchone()[0]
										username = await client.fetch_user(int(user1))
										embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
										embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend}', value='\u200b')
										await message.channel.send(embed=embed4)

										cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
										channelmessageid = cursor.fetchone()[0]
										channelmessageid = client.get_channel(int(channelmessageid))

										cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
										messages = cursor.fetchone()[0]
										try:
											msg101 = await channelmessageid.fetch_message(int(messages))
											await msg101.delete()
										except:
											cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												pass

										delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = {serverid} AND server = {serverid}", (level, ))
										conn.commit()
										
										cursor.execute(f"SELECT GDModCheckedChannelNoSend FROM setup WHERE serverid = {serverid} LIMIT 1")
										try:
											gdmodcheckedchannel = cursor.fetchone()[0]
										except TypeError:
											gdmodcheckedchannel = None
										if gdmodcheckedchannel is not None:
											channelmod = client.get_channel(int(gdmodcheckedchannel))
											
											embed13.add_field(name=f"{notsendserver} {gdmodname}. <:error:472907618386575370>\n\n{reasonserver} {reason}", value="\u200b")
											embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/693237079538270261.png?v=1")
	
											description += '=' * (-len(description) % 4)
											base64_bytes = description.encode('ascii')
											
											message_bytes = base64.urlsafe_b64decode(base64_bytes)
											descbase64 = message_bytes.decode('ascii')

											if int(objectplus) >= 40000:
												embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {byserver} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
											elif int(objectplus) <= 39999:
												embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {byserver} {creator}', value=f"{desc} {descbase64}", inline=False)

											if int(coins) == 0:
												coinsvalue = f"{none}"
											elif int(coins) == 1:
												coinsvalue = "<:user_coin_unverified:472908993832943631>"
											elif int(coins) == 2:
												coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
											elif int(coins) == 3:
												coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

											try:
												if int(verifiedcoins) == 1:
													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin:472908993711308800>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
											except ValueError:
												pass

											embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

											#reqsearch2(level)
											try:
												songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
											except ValueError:
												songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

											songlink2 = unquote(f"{songlink}")
											try:
												officialsong2 = int(officialsong)
											except UnboundLocalError:
												embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
											else:
												embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
											
											await channelmod.send(f"<@{user1}>",embed=embed13)
											return
									else:
										nyaya = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
										user1 = cursor.fetchone()[0]
										username = await client.fetch_user(int(user1))

										cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
										try:
											language_requester = cursor.fetchone()[0]
										except TypeError:
											language_requester = language_default
										language2_requester = language_requester
										translate_messages_requester = open(f"language/requester/reqnotsend/{language2}.txt").read().splitlines()

										successtitlerequester = translate_messages_requester[0]
										thelevelyourequested = translate_messages_requester[1]
										byrequester = translate_messages_requester[2]
										notsendrequester = translate_messages_requester[3]
										reasonrequester = translate_messages_requester[4]

										await msg.delete()
										papa = cursor.execute(f"SELECT moderatorname FROM GDmoderators WHERE userid = {author} LIMIT 1")
										gdmodname = cursor.fetchone()[0]
										embed3 = discord.Embed(title=f'{successtitlerequester}', color=0xff0000)
										embed3.set_thumbnail(url="https://cdn.discordapp.com/emojis/693237079538270261.png?v=1")
										embed3.add_field(name=f'{thelevelyourequested} `{level}` (**{levelname}** {byrequester} **{creator}**) {notsendrequester} {gdmodname}.', value='\u200b')
										channel = await username.create_dm()
										try:
											await channel.send(embed=embed3)
										except discord.errors.Forbidden:
											pass
										
										nani = cursor.execute(f"SELECT requester FROM levels WHERE levelid = %s AND server = %s LIMIT 1", (level, serverid))
										user1 = cursor.fetchone()[0]
										username = await client.fetch_user(int(user1))
										embed4 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
										embed4.add_field(name=f'{thelevel} `{level}` (**{levelname}** {by} **{creator}**) {successsend}', value='\u200b')
										await message.channel.send(embed=embed4)

										cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
										channelmessageid = cursor.fetchone()[0]
										channelmessageid = client.get_channel(int(channelmessageid))

										cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
										messages = cursor.fetchone()[0]
										try:
											msg101 = await channelmessageid.fetch_message(int(messages))
											await msg101.delete()
										except:
											cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
											channelmessageid = cursor.fetchone()[0]
											channelmessageid = client.get_channel(int(channelmessageid))
											try:
												msg101 = await channelmessageid.fetch_message(int(messages))
												await msg101.delete()
											except:
												pass

										delete = cursor.execute(f"DELETE FROM levels WHERE levelid = %s and server = {serverid} AND server = {serverid}", (level, ))
										conn.commit()
										
										cursor.execute(f"SELECT GDModCheckedChannelNoSend FROM setup WHERE serverid = {serverid} LIMIT 1")
										try:
											gdmodcheckedchannel = cursor.fetchone()[0]
										except TypeError:
											gdmodcheckedchannel = None
										if gdmodcheckedchannel is not None:
											channelmod = client.get_channel(int(gdmodcheckedchannel))
											
											embed13.add_field(name=f"{notsendserver} {gdmodname}. <:error:472907618386575370>", value="\u200b")
											embed13.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/693237079538270261.png?v=1")
	
											description += '=' * (-len(description) % 4)
											base64_bytes = description.encode('ascii')
											
											message_bytes = base64.urlsafe_b64decode(base64_bytes)
											descbase64 = message_bytes.decode('ascii')

											if int(objectplus) >= 40000:
												embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {byserver} {creator} <:object_overflow:472908865953071115>', value=f"{desc} {descbase64}", inline=False)
											elif int(objectplus) <= 39999:
												embed13.add_field(name=f'<:play:472908887859789835> __{levelname}__ {byserver} {creator}', value=f"{desc} {descbase64}", inline=False)

											if int(coins) == 0:
												coinsvalue = f"{none}"
											elif int(coins) == 1:
												coinsvalue = "<:user_coin_unverified:472908993832943631>"
											elif int(coins) == 2:
												coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"
											elif int(coins) == 3:
												coinsvalue = "<:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631> <:user_coin_unverified:472908993832943631>"

											try:
												if int(verifiedcoins) == 1:
													if int(coins) == 0:
														coinsvalue = f"{none}"
													elif int(coins) == 1:
														coinsvalue = "<:user_coin:472908993711308800>"
													elif int(coins) == 2:
														coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800>"
													elif int(coins) == 3:
														coinsvalue = "<:user_coin:472908993711308800> <:user_coin:472908993711308800> <:user_coin:472908993711308800>"
											except ValueError:
												pass

											embed13.add_field(name=f'{coinstitle}: {coinsvalue}', value=f"<:downloads:472907713727430658> `{downloads}`\n{likesemote} `{likes}`\n<:length:472908680459976704> `{lengthvalue}`\n", inline=False)

											#reqsearch2(level)
											try:
												songname,songauthor,songid,sizesong,songlink,officialsong = reqsearch2(level)
											except ValueError:
												songname,songauthor,songid,sizesong,songlink = reqsearch2(level)

											songlink2 = unquote(f"{songlink}")
											try:
												officialsong2 = int(officialsong)
											except UnboundLocalError:
												embed13.add_field(name=f':musical_note:  __{songname}__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{downloadsong}]({songlink2})", inline=False)
											else:
												embed13.add_field(name=f':musical_note: :white_check_mark:   __**{songname}**__ {by} {songauthor}', value=f"SongID: {songid} - {sizetitle}: {sizesong}MB\n<:play:472908887859789835> [{newgroundsplay}](https://newgrounds.com/audio/load/{songid}) <:download_song:472907696685711370> [{youtubelink}]({songlink2})", inline=False)
											
											await channelmod.send(f"<@{user1}>",embed=embed13)
											return
							else:
								await msg.delete()
								embed = discord.Embed(title="", color=0xff0000)
								embed.add_field(name=f'{errormessage}', value=f"{errorban}")
								msg2 = await message.channel.send(embed=embed)
								time.sleep(5)
								await msg2.delete()
								return
						else:
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f'{errorblacklist}')
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
					else:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errorpermission}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
							
				else:
					await msg.delete()
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorpermission}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

		if msg.startswith("report"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqreport"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				try:
					level = args[1]
				except IndexError as error:
					level = "no"
				jaj = message.author.id
				jaj2 = message.author.name

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqsend/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				erroridinvalid = translate_messages[4]
				erroridalreadysubmitted = translate_messages[5]
				erroridempty = translate_messages[6]
				errorban = translate_messages[7]

				successtitle = translate_messages[9]
				by = translate_messages[10]
				successmoderation = translate_messages[11]
				
				translate_cooldown_messages = open(f"language/client/cooldown-{language2}.txt").read().splitlines()
				errorcooldown1 = translate_cooldown_messages[0]
				errorcooldown2 = translate_cooldown_messages[1]
				
				#cooldowncheck(author)
				alwayscooldown,secondcooldown = cooldowncheck(author)
				
				if alwayscooldown == 1:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorcooldown1} {secondcooldown} {errorcooldown2}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				sql = "INSERT INTO cooldowns (userid, cooldown) VALUES (%s, %s)"
				datetime_object_cooldown = datetime_object + datetime.timedelta(seconds=30)
				val = (author, datetime_object_cooldown)
				cursor.execute(sql,val)
				conn.commit()
				
				embed = discord.Embed(title="", color=0x00ff00)
				data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={level}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
				result = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
				if result == "-1":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{erroridinvalid}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				else:
					embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
					embed.add_field(name=f'{loadingdesc}', value="\u200b")
					msg = await message.channel.send(embed=embed)
					pog = cursor.execute(f"SELECT levelid FROM reports WHERE levelid = %s LIMIT 1", (level, ))
					maybe_number = cursor.fetchone()
					if maybe_number is not None:
						number = maybe_number[0]
						await asyncio.sleep(3)
						if level == str(number):
							await msg.delete()
							embed = discord.Embed(title="", color=0xff0000)
							#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
							embed.add_field(name=f'{errormessage}', value=f'{erroridalreadysubmitted}')
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
					if maybe_number == "no":
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{erroridempty}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
					else:
						poggare = cursor.execute(f"SELECT userid FROM banned WHERE userid = {jaj} LIMIT 1")
						maybe_number3 = cursor.fetchone()
						if maybe_number3 is None:
							result = result.split(":")
							levelname = result[3]
							creator = convertinfo("u","n",result[7])
							sql = "INSERT INTO reports (levelid, isBlacklist) VALUES (%s, %s)"
							var = (level, 0)
							cursor.execute(sql, var)
							conn.commit()
							await asyncio.sleep(3)
							await msg.delete()

							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f'`{level}` (**{levelname}** {by} **{creator}**) {successmoderation}', value='\u200b')
							await message.channel.send(embed=embed)
							embed3 = discord.Embed(title=f'New report sent by {jaj2} (`{jaj}`)! <:downloads:472907713727430658>', color=0x00ff00)
							embed3.add_field(name=f'`{level}` (**{levelname}** by **{creator}**)', value='\u200b')
							embed3.set_footer(text=f"{message.guild.name} --- {message.author}")
							channel2 = client.get_channel(int(718103983217967165))
							await channel2.send(f"<@&718062047362941061>",embed=embed3)
							return
						else:
							await msg.delete()
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorban}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return

		if msg.startswith("mod approve"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqmodapprove"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				try:
					level = args[2]
				except IndexError as error:
					level = 0

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqmod approve/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorpermission = translate_messages[4]
				errornotfound = translate_messages[5]

				successtitle = translate_messages[7]
				successblacklist = translate_messages[8]

				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)
				pogygy = cursor.execute(f"SELECT userid FROM GRmoderators WHERE userid = {author} LIMIT 1")
				role = cursor.fetchone()
				if role is None:
					await msg.delete()
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorpermission}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return
				else:
					pog = cursor.execute(f"SELECT levelid FROM reports WHERE levelid = %s LIMIT 1", (level, ))
					try:
						maybe_number = cursor.fetchone()[0]
					except TypeError as error:
						maybe_number = 0
					if str(maybe_number) == level:
						number = maybe_number
						await asyncio.sleep(3)
						if level == str(number):
							pogger = cursor.execute(f"UPDATE reports SET isBlacklist = 1 WHERE levelid = %s", (level, ))
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title="", color=0x00ff00)
							#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
							embed.add_field(name=f'{successtitle}', value=f'{successblacklist}')
							await message.channel.send(embed=embed)
							return
						return
					else:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
						embed.add_field(name=f'{errormessage}', value=f'{errornotfound}')
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return

		if msg.startswith("mod unapprove"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqmodunapprove"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				try:
					level = args[2]
				except IndexError as error:
					level = 0

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqmod unapprove/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorpermission = translate_messages[4]
				errornotfound = translate_messages[5]

				successtitle = translate_messages[7]
				successblacklist = translate_messages[8]

				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)
				pogygy = cursor.execute(f"SELECT userid FROM GRmoderators WHERE userid = {author} LIMIT 1")
				role = cursor.fetchone()
				if role is None:
					await msg.delete()
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorpermission}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return
				else:
					pog = cursor.execute(f"SELECT levelid FROM reports WHERE levelid = %s LIMIT 1", (level, ))
					try:
						maybe_number = cursor.fetchone()[0]
					except TypeError as error:
						maybe_number = 0
					if str(maybe_number) == level:
						number = maybe_number
						await asyncio.sleep(3)
						if level == str(number):
							pogger = cursor.execute(f"DELETE FROM reports WHERE levelid = %s", (level, ))
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title="", color=0x00ff00)
							#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
							embed.add_field(name=f'{successtitle}', value=f'{successblacklist}')
							await message.channel.send(embed=embed)
							return
						return
					else:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
						embed.add_field(name=f'{errormessage}', value=f'{errornotfound}')
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return

		if msg.startswith("mod ban"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqmodban"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				try:
					user1 = args[2]
				except IndexError as error:
					user1 = 0

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqmod ban/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorpermission = translate_messages[4]
				erroralreadybanned = translate_messages[5]
				errorsyntaxuser = translate_messages[6]

				successtitle = translate_messages[8]
				successban1 = translate_messages[9]
				successban2 = translate_messages[10]

				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)
				conn.commit()
				pogygy = cursor.execute(f"SELECT userid FROM GRmoderators WHERE userid = {author} LIMIT 1")
				role = cursor.fetchone()
				if role is None:
					await msg.delete()
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorpermission}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return
				else:
					try:
						pog = cursor.execute(f"INSERT INTO banned (userid) VALUES ({user1})")
					except MC.Error as error:
						if error.errno == errorcode.ER_DUP_ENTRY:
							await msg.delete()
							embed2 = discord.Embed(title="", color=0xff0000)
							embed2.add_field(name=f'{errormessage}', value=f"{erroralreadybanned}")
							msg2 = await message.channel.send(embed=embed2)
							time.sleep(5)
							await msg2.delete()
							return
						else:
							print(error)
					else:
						if user1 == 0:
							await msg.delete()
							embed = discord.Embed(title="", color=0xff0000)
							#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
							embed.add_field(name=f'{errormessage}', value=f'{errorsyntaxuser}')
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						username = await client.fetch_user(int(user1))
						if username is None:
							await msg.delete()
							embed = discord.Embed(title="", color=0xff0000)
							#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
							embed.add_field(name=f'{errormessage}', value=f'{errorsyntaxuser}')
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						else:
							await asyncio.sleep(3)
							await msg.delete()

							username = await client.fetch_user(int(user1))
							embed3 = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed3.add_field(name=f"{successban1} `{username}` {successban2}", value='\u200b')

							cursor.execute(f"SELECT language FROM users WHERE userid = {user1}")
							try:
								language_requester = cursor.fetchone()[0]
							except TypeError:
								language_requester = language_default
							language2_requester = language_requester
							translate_messages_requester = open(f"language/requester/reqmod ban/{language2}.txt").read().splitlines()

							bantitle = translate_messages_requester[0]
							bandesc = translate_messages_requester[1]

							embed4 = discord.Embed(title="", color=0xff0000)
							embed4.add_field(name=f'{bantitle}', value=f"{bandesc}")
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed4)
							except discord.errors.Forbidden:
								pass
							await message.channel.send(embed=embed3)
							return

		if msg.startswith("mod unban"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqmodunban"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

				try:
					user = args[2]
				except IndexError as error:
					user = 0

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqmod unban/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorpermission = translate_messages[4]
				errorsyntaxuser = translate_messages[5]

				successtitle = translate_messages[7]
				successunban1 = translate_messages[8]
				successunban2 = translate_messages[9]

				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)
				pogygy = cursor.execute(f"SELECT userid FROM GRmoderators WHERE userid = {author} LIMIT 1")
				role = cursor.fetchone()
				if role is None:
					await msg.delete()
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorpermission}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return
				else:
					if user == 0:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
						embed.add_field(name=f'{errormessage}', value=f'{errorsyntaxuser}')
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
					username = await client.fetch_user(int(user))
					if username is None:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
						embed.add_field(name=f'{errormessage}', value=f'{errorsyntaxuser}')
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
					else:
						pog = cursor.execute(f"DELETE FROM banned WHERE userid = {user}")
						conn.commit()
						await asyncio.sleep(3)
						await msg.delete()

						embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
						username = await client.fetch_user(int(user))

						cursor.execute(f"SELECT language FROM users WHERE userid = {user}")
						try:
							language_requester = cursor.fetchone()[0]
						except TypeError:
							language_requester = language_default
						language2_requester = language_requester
						translate_messages_requester = open(f"language/requester/reqmod unban/{language2}.txt").read().splitlines()

						unbantitle = translate_messages_requester[0]
						unbandesc = translate_messages_requester[1]

						embed.add_field(name=f'{successunban1} `{username}` {successunban2}', value='\u200b')
						embed2 = discord.Embed(title="", color=0x00ff00)
						embed2.add_field(name=f'{unbantitle}', value=f"{unbandesc}")
						channel = await username.create_dm()
						try:
							await channel.send(embed=embed2)
						except discord.errors.Forbidden:
							pass

						await message.channel.send(embed=embed)
						return

		if msg.startswith("profile link"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqprofilelink"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqprofile link/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				erroraccountalready = translate_messages[4]

				successtitle = translate_messages[6]
				successdesc = translate_messages[7]

				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)
				cursor.execute(f"SELECT userid FROM users WHERE userid = {author}")
				verify = cursor.fetchone()
				if verify is None:
					default = "no"
					zero = 0
					one = 1
					color1 = "0x7dff00"
					color2 = "0x00ffff"
					sql = "INSERT INTO users (userid, levelrequestedcount, levelreviewedcount, levelreviewapprovedcount, levelreviewunapprovedcount, requestachievement1, requestachievement5, requestachievement10, requestachievement50, requestachievement100, reviewachievement1, reviewachievement5, reviewachievement10, reviewachievement50, reviewachievement100, reviewapprovedachievement1, reviewapprovedachievement5, reviewapprovedachievement10, reviewapprovedachievement50, reviewapprovedachievement100, reviewunapprovedachievement1, reviewunapprovedachievement5, reviewunapprovedachievement10, reviewunapprovedachievement50, reviewunapprovedachievement100, levelsentbygdmod, firstsync, suggestidea, approvedidea, approvedreport, language, isCubeUnlocked, cubetype, color1, color2, glowoutline) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					var = (author,zero,zero,zero,zero,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,"yes",default,default,default,"en",one,one,color1,color2,zero)
					cursor.execute(sql, var)
					conn.commit()
					sql = f"INSERT INTO rewards (userid) VALUES ({author})"
					cursor.execute(sql)
					conn.commit()
					await msg.delete()
					embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
					embed.add_field(name=f"{successdesc}", value='\u200b')
					msg1 = await message.channel.send(embed=embed)
					firstsync(author)
					embed5 = firstsync(author)
					username = await client.fetch_user(int(author))
					channel = await username.create_dm()
					try:
						await channel.send(embed=embed5)
					except discord.errors.Forbidden:
						pass
					return
				else:
					await msg.delete()
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{erroraccountalready}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return

		if msg.startswith("profile unlink"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqprofileunlink"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqprofile unlink/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorlink = translate_messages[4]

				successtitle = translate_messages[6]
				successdesc = translate_messages[7]

				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)
				cursor.execute(f"SELECT userid FROM users WHERE userid = {author}")
				verify = cursor.fetchone()
				if verify is None:
					await msg.delete()
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorlink}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return
				else:

					cursor.execute(f"DELETE FROM users WHERE userid = {author}")
					conn.commit()
					cursor.execute(f"DELETE FROM levels WHERE requester = {author}")
					conn.commit()
					cursor.execute(f"DELETE FROM rewards WHERE userid = {author}")
					conn.commit()
					await msg.delete()
					embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
					embed.add_field(name=f"{successdesc}", value='\u200b')
					msg1 = await message.channel.send(embed=embed)
					return

		if msg.startswith("announcement"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqannouncement/{language2}.txt").read().splitlines()

				errormessage = translate_messages[0]
				errortext = translate_messages[1]
				errorpermission = translate_messages[2]

				successtitle = translate_messages[4]
				successdesc = translate_messages[5]

				nametag = message.author
				try:
					text = args[1:]
				except IndexError as error:
					text = None
				if author == jouca:
					if text is None:
						await msg.delete()
						embed = discord.Embed(title="", color=0xff0000)
						#embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/472907618386575370.png")
						embed.add_field(name=f'{errormessage}', value=f'{errortext}')
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
					sentence = ' '.join(text)
					pog = cursor.execute("SELECT AnnouncementBot FROM setup WHERE AnnouncementBot IS NOT NULL")
					row = cursor.fetchone()
					embedyes = discord.Embed(title=f'{successtitle}', color=0x00ff00)
					embedyes.add_field(name=f"{successdesc}", value='\u200b')
					msg1234 = await message.channel.send(embed=embedyes)
					while row is not None:
						channel2 = client.get_channel(int(row[0]))
						embed3 = discord.Embed(title="A message from the developer of Geometry Request", color=0x00ff0)
						if message.attachments:
							fileimage = message.attachments[0]
							imageurl = fileimage.url
							for ext in pic_ext:
								if imageurl.endswith(ext):
									embed3.set_image(url=f"{imageurl}")

						embed3.set_author(name=f"{nametag}", icon_url="https://pbs.twimg.com/profile_images/1260383799537434625/g4M83_3f.jpg")
						embed3.add_field(name='Announcement Bot', value=f"{sentence}")
						try:
							await channel2.send(embed=embed3)
						except discord.errors:
							pass
						row = cursor.fetchone()
					return
				else:
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorpermission}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return

		if msg.startswith("eval"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor()
				
				args = [x for ar in args for x in ar.split('\n')]

				embed3 = discord.Embed(title="<:info:472908656514433064> Loading...", color=0xffce08)
				embed3.add_field(name='Loading... Please wait a little moment', value="\u200b")
				loading	= await message.channel.send(embed=embed3)
				server = message.guild.name
				var = message.guild.id
				author = message.author.id
				channel = message.channel.id

				query = " ".join(msg.split(" ")[1:])
				if author != jouca:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name='Error. <:error:472907618386575370>', value="You are not Jouca.")
					await message.channel.send(embed=embed)
					await loading.delete()
					return

				if len(query) == 0:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name='Error. <:error:472907618386575370>', value="You need to input a query.")
					await message.channel.send(embed=embed)
					await loading.delete()
					return

				try:
					cursor.execute(query)
				except MC.Error as error:
					embed = discord.Embed(title="Error. <:error:472907618386575370>", color=0xff0000)
					embed.add_field(name='Input :inbox_tray:', value=f"```{query}```")
					embed.add_field(name='Output :outbox_tray:', value=error, inline=False)
					await loading.delete()
					await message.channel.send(embed=embed)
					return
				commitlist = ["INSERT","UPDATE","DELETE"]
				embed = discord.Embed(title='Success! <:success:472908961176092702>', color=0x00ff00)
				embed.add_field(name='Input :inbox_tray:', value=f"```{query}```")
				if query.split(" ")[0] in commitlist:
					conn.commit()
					embed.add_field(name='Output :outbox_tray:', value="OK! <:success:472908961176092702>", inline=False)
					await loading.delete()
					await message.channel.send(embed=embed)
					return
				else:
					result = cursor.fetchall()
					embed.add_field(name='Output :outbox_tray:', value=f"```{result}```", inline=False)
					await loading.delete()
					await message.channel.send(embed=embed)
					return

		if msg.startswith("exec"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor()
				args = [x for ar in args for x in ar.split('\n')]

				embed3 = discord.Embed(title="<:info:472908656514433064> Loading...", color=0xffce08)
				embed3.add_field(name='Loading... Please wait a little moment', value="\u200b")
				loading	= await message.channel.send(embed=embed3)
				server = message.guild.name
				var = message.guild.id
				author = message.author.id
				channel = message.channel.id
				query = " ".join(msg.split(" ")[1:])
				if author != jouca: #553971625679126549
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name='Error. <:error:472907618386575370>', value="You are not Jouca.")
					await message.channel.send(embed=embed)
					await loading.delete()
					return
				if len(query) == 0:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name='Error. <:error:472907618386575370>', value="You need to input code.")
					await message.channel.send(embed=embed)
					await loading.delete()
					return
				try:
					embed = discord.Embed(title='Success! <:success:472908961176092702>', color=0x00ff00)
					embed.add_field(name='Input :inbox_tray:', value=f"```{query}```")
					env = {
						"message": message,
						"cursor": cursor,
						"conn": conn
					}
					res = exec(query, env);
					embed.add_field(name='Output :outbox_tray:', value=f"```{res}```", inline=False)
					await loading.delete()
					await message.channel.send(embed=embed)
				except Exception as error:
					embed = discord.Embed(title="Error. <:error:472907618386575370>", color=0xff0000)
					embed.add_field(name='Input :inbox_tray:', value=f"```{query}```")
					embed.add_field(name='Output :outbox_tray:', value=error, inline=False)
					await loading.delete()
					await message.channel.send(embed=embed)
					return
				return
			return;

		if msg.startswith("achievements"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqachievements"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqachievements/{language2}.txt").read().splitlines()

				errormessage = translate_messages[0]
				errorlink = translate_messages[1]

				achievementtitle1 = translate_messages[3]
				achievementtitle2 = translate_messages[4]
				achievementdesc = translate_messages[5]
				achievementtitle = translate_messages[6]
				information = translate_messages[7]
				page = translate_messages[8]
				reactions = translate_messages[9]

				firstsync = translate_messages[11]
				requestachievement1 = translate_messages[12]
				requestachievement5 = translate_messages[13]
				requestachievement10 = translate_messages[14]
				requestachievement50 = translate_messages[15]
				requestachievement100 = translate_messages[16]

				reviewachievement1 = translate_messages[18]
				reviewachievement5 = translate_messages[19]
				reviewachievement10 = translate_messages[20]
				reviewachievement50 = translate_messages[21]
				reviewachievement100 = translate_messages[22]

				reviewapprovedachievement1 = translate_messages[24]
				reviewapprovedachievement5 = translate_messages[25]
				reviewapprovedachievement10 = translate_messages[26]
				reviewapprovedachievement50 = translate_messages[27]
				reviewapprovedachievement100 = translate_messages[28]

				reviewunapprovedachievement1 = translate_messages[30]
				reviewunapprovedachievement5 = translate_messages[31]
				reviewunapprovedachievement10 = translate_messages[32]
				reviewunapprovedachievement50 = translate_messages[33]
				reviewunapprovedachievement100 = translate_messages[34]

				levelsentbygdmod = translate_messages[36]
				suggestidea = translate_messages[37]
				approvedidea = translate_messages[38]
				approvedreport = translate_messages[39]

				nametag = message.author

				cursor.execute(f"SELECT userid FROM users WHERE userid = {author}")
				linked = cursor.fetchone()
				if linked is None:
					await msg.delete()
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorlink}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

				cursor.execute(f"SELECT * FROM users WHERE userid = {author} LIMIT 1")
				result = cursor.fetchone()

				percentagecount = 0

				achievement1 = result[27]
				if achievement1 == "no":
					achievement1b = "<:lock:472908825578569728>"
				elif achievement1 == "yes":
					achievement1b = "<:success:472908961176092702>"
					percentagecount += 1

				reqcount = result[2]
				achievement2 = result[6]
				if achievement2 == "no":
					achievement2b = f"<:lock:472908825578569728> ({reqcount}/1)"
				elif achievement2 == "yes":
					achievement2b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement3 = result[7]
				if achievement3 == "no":
					achievement3b = f"<:lock:472908825578569728> ({reqcount}/5)"
				elif achievement3 == "yes":
					achievement3b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement4 = result[8]
				if achievement4 == "no":
					achievement4b = f"<:lock:472908825578569728> ({reqcount}/10)"
				elif achievement4 == "yes":
					achievement4b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement5 = result[9]
				if achievement5 == "no":
					achievement5b = f"<:lock:472908825578569728> ({reqcount}/50)"
				elif achievement5 == "yes":
					achievement5b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement6 = result[10]
				if achievement6 == "no":
					achievement6b = f"<:lock:472908825578569728> ({reqcount}/100)"
				elif achievement6 == "yes":
					achievement6b = "<:success:472908961176092702>"
					percentagecount += 1

				reviewcount = result[3]
				achievement7 = result[11]
				if achievement7 == "no":
					achievement7b = f"<:lock:472908825578569728> ({reviewcount}/1)"
				elif achievement7 == "yes":
					achievement7b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement8 = result[12]
				if achievement8 == "no":
					achievement8b = f"<:lock:472908825578569728> ({reviewcount}/5)"
				elif achievement8 == "yes":
					achievement8b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement9 = result[13]
				if achievement9 == "no":
					achievement9b = f"<:lock:472908825578569728> ({reviewcount}/10)"
				elif achievement9 == "yes":
					achievement9b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement10 = result[14]
				if achievement10 == "no":
					achievement10b = f"<:lock:472908825578569728> ({reviewcount}/50)"
				elif achievement10 == "yes":
					achievement10b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement11 = result[15]
				if achievement11 == "no":
					achievement11b = f"<:lock:472908825578569728> ({reviewcount}/100)"
				elif achievement11 == "yes":
					achievement11b = "<:success:472908961176092702>"
					percentagecount += 1

				approvedreviewcount = result[4]
				achievement12 = result[16]
				if achievement12 == "no":
					achievement12b = f"<:lock:472908825578569728> ({approvedreviewcount}/1)"
				elif achievement12 == "yes":
					achievement12b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement13 = result[17]
				if achievement13 == "no":
					achievement13b = f"<:lock:472908825578569728> ({approvedreviewcount}/5)"
				elif achievement13 == "yes":
					achievement13b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement14 = result[18]
				if achievement14 == "no":
					achievement14b = f"<:lock:472908825578569728> ({approvedreviewcount}/10)"
				elif achievement14 == "yes":
					achievement14b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement15 = result[19]
				if achievement15 == "no":
					achievement15b = f"<:lock:472908825578569728> ({approvedreviewcount}/50)"
				elif achievement15 == "yes":
					achievement15b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement16 = result[20]
				if achievement16 == "no":
					achievement16b = f"<:lock:472908825578569728> ({approvedreviewcount}/100)"
				elif achievement16 == "yes":
					achievement16b = "<:success:472908961176092702>"
					percentagecount += 1

				unapprovedreviewcount = result[5]
				achievement17 = result[21]
				if achievement17 == "no":
					achievement17b = f"<:lock:472908825578569728> ({unapprovedreviewcount}/1)"
				elif achievement17 == "yes":
					achievement17b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement18 = result[22]
				if achievement18 == "no":
					achievement18b = f"<:lock:472908825578569728> ({unapprovedreviewcount}/5)"
				elif achievement18 == "yes":
					achievement18b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement19 = result[23]
				if achievement19 == "no":
					achievement19b = f"<:lock:472908825578569728> ({unapprovedreviewcount}/10)"
				elif achievement19 == "yes":
					achievement19b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement20 = result[24]
				if achievement20 == "no":
					achievement20b = f"<:lock:472908825578569728> ({unapprovedreviewcount}/50)"
				elif achievement20 == "yes":
					achievement20b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement21 = result[25]
				if achievement21 == "no":
					achievement21b = f"<:lock:472908825578569728> ({unapprovedreviewcount}/100)"
				elif achievement21 == "yes":
					achievement21b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement22 = result[26]
				if achievement22 == "no":
					achievement22b = "<:lock:472908825578569728>"
				elif achievement22 == "yes":
					achievement22b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement23 = result[28]
				if achievement23 == "no":
					achievement23b = "<:lock:472908825578569728>"
				elif achievement23 == "yes":
					achievement23b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement24 = result[29]
				if achievement24 == "no":
					achievement24b = "<:lock:472908825578569728>"
				elif achievement24 == "yes":
					achievement24b = "<:success:472908961176092702>"
					percentagecount += 1

				achievement25 = result[30]
				if achievement25 == "no":
					achievement25b = "<:lock:472908825578569728>"
				elif achievement25 == "yes":
					achievement25b = "<:success:472908961176092702>"
					percentagecount += 1

				percentage2 = percentagecount/25*100
				percentage = round(percentage2, 2)
				embed1 = discord.Embed(title=f"{achievementtitle1} ({percentage}% {achievementtitle2})", color=0xa55cff)
				embed1.set_author(name=f"{achievementdesc}", icon_url="https://cdn.discordapp.com/emojis/472908825578569728.png?v=1")
				embed2 = discord.Embed(title=f"{achievementtitle1} ({percentage}% {achievementtitle2})", color=0xa55cff)
				embed2.set_author(name=f"{achievementdesc}", icon_url="https://cdn.discordapp.com/emojis/472908825578569728.png?v=1")
				embed3 = discord.Embed(title=f"{achievementtitle1} ({percentage}% {achievementtitle2})", color=0xa55cff)
				embed3.set_author(name=f"{achievementdesc}", icon_url="https://cdn.discordapp.com/emojis/472908825578569728.png?v=1")
				embed4 = discord.Embed(title=f"{achievementtitle1} ({percentage}% {achievementtitle2})", color=0xa55cff)
				embed4.set_author(name=f"{achievementdesc}", icon_url="https://cdn.discordapp.com/emojis/472908825578569728.png?v=1")
				embed5 = discord.Embed(title=f"{achievementtitle1} ({percentage}% {achievementtitle2})", color=0xa55cff)
				embed5.set_author(name=f"{achievementdesc}", icon_url="https://cdn.discordapp.com/emojis/472908825578569728.png?v=1")

				embed1.add_field(name=f"{achievementtitle}", value=f"{firstsync} {achievement1b}\n\n{requestachievement1} {achievement2b}\n{requestachievement5} {achievement3b}\n{requestachievement10} {achievement4b}\n{requestachievement50} {achievement5b}\n{requestachievement100} {achievement6b}", inline=False)
				embed2.add_field(name=f"{achievementtitle}", value=f"{reviewachievement1} {achievement7b}\n{reviewachievement5} {achievement8b}\n{reviewachievement10} {achievement9b}\n{reviewachievement50} {achievement10b}\n{reviewachievement100} {achievement11b}", inline=False)
				embed3.add_field(name=f"{achievementtitle}", value=f"{reviewapprovedachievement1} {achievement12b}\n{reviewapprovedachievement5} {achievement13b}\n{reviewapprovedachievement10} {achievement14b}\n{reviewapprovedachievement50} {achievement15b}\n{reviewapprovedachievement100} {achievement16b}", inline=False)
				embed4.add_field(name=f"{achievementtitle}", value=f"{reviewunapprovedachievement1} {achievement17b}\n{reviewunapprovedachievement5} {achievement18b}\n{reviewunapprovedachievement10} {achievement19b}\n{reviewunapprovedachievement50} {achievement20b}\n{reviewunapprovedachievement100} {achievement21b}", inline=False)
				embed5.add_field(name=f"{achievementtitle}", value=f"{levelsentbygdmod} {achievement22b}\n\n{suggestidea} {achievement23b}\n{approvedidea} {achievement24b}\n\n{approvedreport} {achievement25b}", inline=False)

				embed1.add_field(name=f"{information}", value=f"{page} 1/5 - {reactions}", inline=False)
				embed2.add_field(name=f"{information}", value=f"{page} 2/5 - {reactions}", inline=False)
				embed3.add_field(name=f"{information}", value=f"{page} 3/5 - {reactions}", inline=False)
				embed4.add_field(name=f"{information}", value=f"{page} 4/5 - {reactions}", inline=False)
				embed5.add_field(name=f"{information}", value=f"{page} 5/5 - {reactions}", inline=False)

				messages = (embed1, embed2, embed3, embed4, embed5)

				index = 0
				msg = None
				action = message.channel.send
				while True:
					res = await action(embed=messages[index])
					if res is not None:
						msg = res
					l = index != 0
					r = index != len(messages) - 1
					if l:
						await msg.add_reaction(left)
					if r:
						await msg.add_reaction(right)
					try:
						react, user = await client.wait_for('reaction_add', check=predicate(msg, l, r), timeout=30)
					except Exception:
						print("BROKE")
						break
					if react.emoji == left:
						index -= 1
					elif react.emoji == right:
						index += 1
					action = msg.edit
				return

		if msg.startswith("achievement give"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqachievementgive"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				args = [x for ar in args for x in ar.split('\n')]

				authorid = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {authorid}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqachievement give/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorsyntax = translate_messages[4]
				errorlink = translate_messages[5]
				errorpermission = translate_messages[6]

				successtitle = translate_messages[8]
				successdesc = translate_messages[9]

				nametag = message.author
				try:
					achievement = args[2]
				except IndexError as error:
					achievement = None
				try:
					user = args[3]
					user1 = args[3]
					author = args[3]
				except IndexError as error:
					user = 0
					user1 = 0
					author = 0
				if authorid == jouca:
					embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
					embed.add_field(name=f'{loadingdesc}', value="\u200b")
					msg = await message.channel.send(embed=embed)
					cursor.execute(f'SELECT userid FROM users WHERE userid = {user}')
					try:
						result = cursor.fetchone()[0]
					except TypeError:
						result = None
					if result is not None:
						if achievement == "requestachievement1":
							cursor.execute(f'UPDATE users SET requestachievement1 = "yes" WHERE userid = {user}')
							conn.commit()
							#requestachievement1(author)
							embed5 = requestachievement1(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "requestachievement5":
							cursor.execute(f'UPDATE users SET requestachievement5 = "yes" WHERE userid = {user}')
							conn.commit()
							#requestachievement5(author)
							embed5 = requestachievement5(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "requestachievement10":
							cursor.execute(f'UPDATE users SET requestachievement10 = "yes" WHERE userid = {user}')
							conn.commit()
							#requestachievement10(author)
							embed5 = requestachievement10(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "requestachievement50":
							cursor.execute(f'UPDATE users SET requestachievement50 = "yes" WHERE userid = {user}')
							conn.commit()
							#requestachievement50(author)
							embed5 = requestachievement50(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "requestachievement100":
							cursor.execute(f'UPDATE users SET requestachievement100 = "yes" WHERE userid = {user}')
							conn.commit()
							#requestachievement100(author)
							embed5 = requestachievement100(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewachievement1":
							cursor.execute(f'UPDATE users SET reviewachievement1 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewachievement1(author)
							embed5 = reviewachievement1(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewachievement5":
							cursor.execute(f'UPDATE users SET reviewachievement5 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewachievement5(author)
							embed5 = reviewachievement5(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewachievement10":
							cursor.execute(f'UPDATE users SET reviewachievement10 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewachievement10(author)
							embed5 = reviewachievement10(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewachievement50":
							cursor.execute(f'UPDATE users SET reviewachievement50 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewachievement50(author)
							embed5 = reviewachievement50(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewachievement100":
							cursor.execute(f'UPDATE users SET reviewachievement100 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewachievement100(author)
							embed5 = reviewachievement100(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewapprovedachievement1":
							cursor.execute(f'UPDATE users SET reviewapprovedachievement1 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewapprovedachievement1(user1)
							embed5 = reviewapprovedachievement1(user1)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewapprovedachievement5":
							cursor.execute(f'UPDATE users SET reviewapprovedachievement5 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewapprovedachievement5(user1)
							embed5 = reviewapprovedachievement5(user1)
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewapprovedachievement10":
							cursor.execute(f'UPDATE users SET reviewapprovedachievement10 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewapprovedachievement10(user1)
							embed5 = reviewapprovedachievement10(user1)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewapprovedachievement50":
							cursor.execute(f'UPDATE users SET reviewapprovedachievement50 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewapprovedachievement50(user1)
							embed5 = reviewapprovedachievement50(user1)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewapprovedachievement100":
							cursor.execute(f'UPDATE users SET reviewapprovedachievement100 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewapprovedachievement100(user1)
							embed5 = reviewapprovedachievement100(user1)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewunapprovedachievement1":
							cursor.execute(f'UPDATE users SET reviewunapprovedachievement1 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewunapprovedachievement1(user1)
							embed5 = reviewunapprovedachievement1(user1)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewunapprovedachievement5":
							cursor.execute(f'UPDATE users SET reviewunapprovedachievement5 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewunapprovedachievement5(user1)
							embed5 = reviewunapprovedachievement5(user1)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewunapprovedachievement10":
							cursor.execute(f'UPDATE users SET reviewunapprovedachievement10 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewunapprovedachievement10(user1)
							embed5 = reviewunapprovedachievement10(user1)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewunapprovedachievement50":
							cursor.execute(f'UPDATE users SET reviewunapprovedachievement50 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewunapprovedachievement50(user1)
							embed5 = reviewunapprovedachievement50(user1)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewunapprovedachievement100":
							cursor.execute(f'UPDATE users SET reviewunapprovedachievement100 = "yes" WHERE userid = {user}')
							conn.commit()
							reviewunapprovedachievement100(user1)
							embed5 = reviewunapprovedachievement100(user1)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "levelsentbygdmod":
							cursor.execute(f'UPDATE users SET levelsentbygdmod = "yes" WHERE userid = {user}')
							conn.commit()
							levelsentbygdmod(user1)
							embed5 = levelsentbygdmod(user1)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "firstsync":
							cursor.execute(f'UPDATE users SET firstsync = "yes" WHERE userid = {user}')
							conn.commit()
							firstsync(author)
							embed5 = firstsync(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "suggestidea":
							cursor.execute(f'UPDATE users SET suggestidea = "yes" WHERE userid = {user}')
							conn.commit()
							suggestidea(author)
							embed5 = suggestidea(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "approvedidea":
							cursor.execute(f'UPDATE users SET approvedidea = "yes" WHERE userid = {user}')
							conn.commit()
							approvedidea(author)
							embed5 = approvedidea(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "approvedreport":
							cursor.execute(f'UPDATE users SET approvedreport = "yes" WHERE userid = {user}')
							conn.commit()
							approvedreport(author)
							embed5 = approvedreport(author)
							username = await client.fetch_user(int(user))
							channel = await username.create_dm()
							try:
								await channel.send(embed=embed5)
							except discord.errors.Forbidden:
								pass
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						else:
							await msg.delete()
							embed5 = discord.Embed(title="", color=0xff0000)
							embed5.add_field(name=f'{errormessage}', value=f"{errorsyntax}")
							msg2 = await message.channel.send(embed=embed5)
							time.sleep(5)
							await msg2.delete()
							return
					else:
						await msg.delete()
						embed5 = discord.Embed(title="", color=0xff0000)
						embed5.add_field(name=f'{errormessage}', value=f"{errorlink}")
						msg2 = await message.channel.send(embed=embed5)
						time.sleep(5)
						await msg2.delete()
						return
				else:
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorpermission}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return

		if msg.startswith("achievement remove"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqachievementremove"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				args = [x for ar in args for x in ar.split('\n')]

				authorid = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {authorid}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqachievement remove/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorsyntax = translate_messages[4]
				errorlink = translate_messages[5]
				errorpermission = translate_messages[6]

				successtitle = translate_messages[8]
				successdesc = translate_messages[9]

				nametag = message.author
				try:
					achievement = args[2]
				except IndexError as error:
					achievement = None
				try:
					user = args[3]
				except IndexError as error:
					user = 0
				if author == jouca:
					embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
					embed.add_field(name=f'{loadingdesc}', value="\u200b")
					msg = await message.channel.send(embed=embed)
					cursor.execute(f'SELECT userid FROM users WHERE userid = {user}')
					try:
						result = cursor.fetchone()[0]
					except TypeError:
						result = None
					if result is not None:
						if achievement == "requestachievement1":
							cursor.execute(f'UPDATE users SET requestachievement1 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "requestachievement5":
							cursor.execute(f'UPDATE users SET requestachievement5 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "requestachievement10":
							cursor.execute(f'UPDATE users SET requestachievement10 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "requestachievement50":
							cursor.execute(f'UPDATE users SET requestachievement50 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "requestachievement100":
							cursor.execute(f'UPDATE users SET requestachievement100 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewachievement1":
							cursor.execute(f'UPDATE users SET reviewachievement1 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewachievement5":
							cursor.execute(f'UPDATE users SET reviewachievement5 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewachievement10":
							cursor.execute(f'UPDATE users SET reviewachievement10 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewachievement50":
							cursor.execute(f'UPDATE users SET reviewachievement50 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewachievement100":
							cursor.execute(f'UPDATE users SET reviewachievement100 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewapprovedachievement1":
							cursor.execute(f'UPDATE users SET reviewapprovedachievement1 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewapprovedachievement5":
							cursor.execute(f'UPDATE users SET reviewapprovedachievement5 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewapprovedachievement10":
							cursor.execute(f'UPDATE users SET reviewapprovedachievement10 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewapprovedachievement50":
							cursor.execute(f'UPDATE users SET reviewapprovedachievement50 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewapprovedachievement100":
							cursor.execute(f'UPDATE users SET reviewapprovedachievement100 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewunapprovedachievement1":
							cursor.execute(f'UPDATE users SET reviewunapprovedachievement1 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewunapprovedachievement5":
							cursor.execute(f'UPDATE users SET reviewunapprovedachievement5 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewunapprovedachievement10":
							cursor.execute(f'UPDATE users SET reviewunapprovedachievement10 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewunapprovedachievement50":
							cursor.execute(f'UPDATE users SET reviewunapprovedachievement50 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "reviewunapprovedachievement100":
							cursor.execute(f'UPDATE users SET reviewunapprovedachievement100 = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "levelsentbygdmod":
							cursor.execute(f'UPDATE users SET levelsentbygdmod = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "firstsync":
							cursor.execute(f'UPDATE users SET firstsync = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "suggestidea":
							cursor.execute(f'UPDATE users SET suggestidea = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "approvedidea":
							cursor.execute(f'UPDATE users SET approvedidea = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						elif achievement == "approvedreport":
							cursor.execute(f'UPDATE users SET approvedreport = "no" WHERE userid = {user}')
							conn.commit()
							await msg.delete()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f"{successdesc} `{achievement}`.", value='\u200b')
							msg1 = await message.channel.send(embed=embed)
							return
						else:
							await msg.delete()
							embed5 = discord.Embed(title="", color=0xff0000)
							embed5.add_field(name=f'{errormessage}', value=f"{errorsyntax}")
							msg2 = await message.channel.send(embed=embed5)
							time.sleep(5)
							await msg2.delete()
							return
					else:
						await msg.delete()
						embed5 = discord.Embed(title="", color=0xff0000)
						embed5.add_field(name=f'{errormessage}', value=f"{errorlink}")
						msg2 = await message.channel.send(embed=embed5)
						time.sleep(5)
						await msg2.delete()
						return
				else:
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorpermission}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return

		if msg.startswith("profile"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)

				maincommand = "reqprofile"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				args = [x for ar in args for x in ar.split('\n')]

				try:
					userprofile = args[1]
				except IndexError as error:
					userprofile = None

				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqprofile/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorlink = translate_messages[4]
				errorprofile = translate_messages[5]

				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)
				if userprofile is None:
					cursor.execute(f"SELECT userid FROM users WHERE userid = {author} LIMIT 1")
					profile = cursor.fetchone()
					if profile is not None:
						usera = await message.guild.fetch_member(author)
						try:
							iconprofile = usera.avatar_url
						except AttributeError:
							iconprofile = "https://cdn.discordapp.com/embed/avatars/0.png"
						if author == jouca:
							owner = "<:owner:736727797191409694>"
						elif author != jouca:
							owner = ""
						cursor.execute(f"SELECT userid FROM GDmoderators WHERE userid = {author} LIMIT 1")
						try:
							mod = cursor.fetchone()[0]
						except TypeError:
							mod = None
						if mod is not None:
							cursor.execute(f"SELECT Modtype FROM GDmoderators WHERE userid = {author} LIMIT 1")
							modtype = cursor.fetchone()[0]
							if modtype == "Mod":
								modbadge = "<:mod:472908845010780169>"
								eldermodbadge = ""
							elif modtype == "ElderMod":
								modbadge = ""
								eldermodbadge = "<:elder_mod:472907732538884117>"
						elif mod is None :
							modbadge = ""
							eldermodbadge = ""
						cursor.execute(f"SELECT userid FROM GRmoderators WHERE userid = {author} LIMIT 1")
						try:
							modbot = cursor.fetchone()[0]
						except TypeError:
							modbot = None
						if modbot is not None:
							botmod = "<:GRmod:741965487096987739>"
						elif modbot is None:
							botmod = ""
						embed2 = discord.Embed(title=f"", color=0x696969)
						embed2.set_author(name=f"__{message.author}'s profile__", icon_url=(iconprofile))
						cursor.execute(f"SELECT levelrequestedcount,levelreviewedcount,levelreviewapprovedcount,levelreviewunapprovedcount FROM users WHERE userid = {author}")
						datastats = cursor.fetchone()
						levelrequestedcount = datastats[0]
						levelreviewedcount = datastats[1]
						levelreviewapprovedcount = datastats[2]
						levelreviewunapprovedcount = datastats[3]
						'''cursor.execute(f"SELECT (SELECT COUNT(*) FROM users WHERE levelrequestedcount >= {levelrequestedcount}) AS position FROM users WHERE userid = {author}")
						levelrequestedcountposition = cursor.fetchone()[0]'''
						cursor.execute("SELECT userid FROM users ORDER BY levelrequestedcount DESC")
						userslist = cursor.fetchall()
						userslist = [x[0] for x in userslist]
						levelrequestedcountposition = userslist.index(str(author))+1
						if levelrequestedcountposition == 1:
							levelrequestedcountposition = f"(<:top1:759751131114373161> #{levelrequestedcountposition})"
						elif levelrequestedcountposition >= 2 and levelrequestedcountposition <= 10:
							levelrequestedcountposition = f"(<:top10:759751146368925757> #{levelrequestedcountposition})"
						elif levelrequestedcountposition >= 11 and levelrequestedcountposition <= 50:
							levelrequestedcountposition = f"(<:top50:759751162860929054> #{levelrequestedcountposition})"
						elif levelrequestedcountposition >= 51 and levelrequestedcountposition <= 100:
							levelrequestedcountposition = f"(<:top100:759751174580338747> #{levelrequestedcountposition})"
						elif levelrequestedcountposition >= 101 and levelrequestedcountposition <= 500:
							levelrequestedcountposition = f"(<:top500:759751189192900649> #{levelrequestedcountposition})"
						elif levelrequestedcountposition >= 501 and levelrequestedcountposition <= 1000:
							levelrequestedcountposition = f"(<:top1000:759751201246937119> #{levelrequestedcountposition})"
						elif levelrequestedcountposition > 1000:
							levelrequestedcountposition = f"(<:topother:759751236819615765> #{levelrequestedcountposition})"
						cursor.execute("SELECT userid FROM users ORDER BY levelreviewedcount DESC")
						userslist = cursor.fetchall()
						userslist = [x[0] for x in userslist]
						levelreviewedcountposition = userslist.index(str(author))+1
						if levelreviewedcountposition == 1:
							levelreviewedcountposition = f"(<:top1:759751131114373161> #{levelreviewedcountposition})"
						elif levelreviewedcountposition >= 2 and levelreviewedcountposition <= 10:
							levelreviewedcountposition = f"(<:top10:759751146368925757> #{levelreviewedcountposition})"
						elif levelreviewedcountposition >= 11 and levelreviewedcountposition <= 50:
							levelreviewedcountposition = f"(<:top50:759751162860929054> #{levelreviewedcountposition})"
						elif levelreviewedcountposition >= 51 and levelreviewedcountposition <= 100:
							levelreviewedcountposition = f"(<:top100:759751174580338747> #{levelreviewedcountposition})"
						elif levelreviewedcountposition >= 101 and levelreviewedcountposition <= 500:
							levelreviewedcountposition = f"(<:top500:759751189192900649> #{levelreviewedcountposition})"
						elif levelreviewedcountposition >= 501 and levelreviewedcountposition <= 1000:
							levelreviewedcountposition = f"(<:top1000:759751201246937119> #{levelreviewedcountposition})"
						elif levelreviewedcountposition > 1000:
							levelreviewedcountposition = f"(<:topother:759751236819615765> #{levelreviewedcountposition})"
						cursor.execute("SELECT userid FROM users ORDER BY levelreviewapprovedcount DESC")
						userslist = cursor.fetchall()
						userslist = [x[0] for x in userslist]
						levelreviewapprovedcountposition = userslist.index(str(author))+1
						if levelreviewapprovedcountposition == 1:
							levelreviewapprovedcountposition = f"(<:top1:759751131114373161> #{levelreviewapprovedcountposition})"
						elif levelreviewapprovedcountposition >= 2 and levelreviewapprovedcountposition <= 10:
							levelreviewapprovedcountposition = f"(<:top10:759751146368925757> #{levelreviewapprovedcountposition})"
						elif levelreviewapprovedcountposition >= 11 and levelreviewapprovedcountposition <= 50:
							levelreviewapprovedcountposition = f"(<:top50:759751162860929054> #{levelreviewapprovedcountposition})"
						elif levelreviewapprovedcountposition >= 51 and levelreviewapprovedcountposition <= 100:
							levelreviewapprovedcountposition = f"(<:top100:759751174580338747> #{levelreviewapprovedcountposition})"
						elif levelreviewapprovedcountposition >= 101 and levelreviewapprovedcountposition <= 500:
							levelreviewapprovedcountposition = f"(<:top500:759751189192900649> #{levelreviewapprovedcountposition})"
						elif levelreviewapprovedcountposition >= 501 and levelreviewapprovedcountposition <= 1000:
							levelreviewapprovedcountposition = f"(<:top1000:759751201246937119> #{levelreviewapprovedcountposition})"
						elif levelreviewapprovedcountposition > 1000:
							levelreviewapprovedcountposition = f"(<:topother:759751236819615765> #{levelreviewapprovedcountposition})"
						cursor.execute("SELECT userid FROM users ORDER BY levelreviewunapprovedcount DESC")
						userslist = cursor.fetchall()
						userslist = [x[0] for x in userslist]
						levelreviewunapprovedcountposition = userslist.index(str(author))+1
						if levelreviewunapprovedcountposition == 1:
							levelreviewunapprovedcountposition = f"(<:top1:759751131114373161> #{levelreviewunapprovedcountposition})"
						elif levelreviewunapprovedcountposition >= 2 and levelreviewunapprovedcountposition <= 10:
							levelreviewunapprovedcountposition = f"(<:top10:759751146368925757> #{levelreviewunapprovedcountposition})"
						elif levelreviewunapprovedcountposition >= 11 and levelreviewunapprovedcountposition <= 50:
							levelreviewunapprovedcountposition = f"(<:top50:759751162860929054> #{levelreviewunapprovedcountposition})"
						elif levelreviewunapprovedcountposition >= 51 and levelreviewunapprovedcountposition <= 100:
							levelreviewunapprovedcountposition = f"(<:top100:759751174580338747> #{levelreviewunapprovedcountposition})"
						elif levelreviewunapprovedcountposition >= 101 and levelreviewunapprovedcountposition <= 500:
							levelreviewunapprovedcountposition = f"(<:top500:759751189192900649> #{levelreviewunapprovedcountposition})"
						elif levelreviewunapprovedcountposition >= 501 and levelreviewunapprovedcountposition <= 1000:
							levelreviewunapprovedcountposition = f"(<:top1000:759751201246937119> #{levelreviewunapprovedcountposition})"
						elif levelreviewunapprovedcountposition > 1000:
							levelreviewunapprovedcountposition = f"(<:topother:759751236819615765> #{levelreviewunapprovedcountposition})"
						embed2.add_field(name=f'{owner}{botmod}{eldermodbadge}{modbadge} {message.author}', value=f"<:requests:726371180508086283> Levels Requested : `{levelrequestedcount}` {levelrequestedcountposition}\n<:reviewed:726371160589205524> Levels Reviewed : `{levelreviewedcount}` {levelreviewedcountposition}\n<:approved:726371180075810816> Levels Approved : `{levelreviewapprovedcount}` {levelreviewapprovedcountposition}\n<:unapproved:726371181875429406> Levels Unapproved : `{levelreviewunapprovedcount}` {levelreviewunapprovedcountposition}", inline=False)
						if author == jouca:
							ownertext = "<:owner:736727797191409694> OWNER\n"
						elif author != jouca:
							ownertext = ""
						if modbot is not None:
							modbottext = "<:GRmod:741965487096987739> GEOMETRY REQUESTS MODERATOR\n"
						elif modbot is None:
							modbottext = ""
						if mod is not None:
							if modtype == "Mod":
								modtext = "<:mod:472908845010780169> GD MODERATOR"
							elif modtype == "ElderMod":
								modtext = "<:elder_mod:472907732538884117> GD ELDER MODERATOR"
						elif mod is None:
							modtext = ""
						ranks = f"{ownertext}{modbottext}{modtext}"
						embed2.add_field(name=f'───────────', value=f"**{ranks}\n<:discord:472907660065505300> Discord : {message.author}**", inline=False)
						embed2.add_field(name=f'───────────', value=f"_For settings, use `req!settings profile`_", inline=False)
						cursor.execute(f"SELECT ID FROM users WHERE userid = {author}")
						accountid = cursor.fetchone()[0]
						embed2.set_footer(text=f"AccountID : {accountid}")

						cursor.execute(f"SELECT isCubeUnlocked FROM users WHERE userid = {author}")
						iscubeunlocked = cursor.fetchone()[0]
						if iscubeunlocked == 1:
							cursor.execute(f"SELECT cubetype FROM users WHERE userid = {author}")
							icontypeid = cursor.fetchone()[0]
							cursor.execute(f"SELECT color1,color2 FROM users WHERE userid = {author}")
							icons = cursor.fetchone()
							color1 = int(icons[0],base=16)
							color2 = int(icons[1],base=16)
							cursor.execute(f"SELECT glowoutline FROM users WHERE userid = {author}")
							glowoutline = cursor.fetchone()[0]
							if glowoutline == 0:
								glowoutline = False
							elif glowoutline == 1:
								glowoutline = True
							image = gd.factory.generate(icon_type="cube", icon_id=int(icontypeid), color_1=gd.Color(color1), color_2=gd.Color(color2), glow_outline=glowoutline)
							buffer = io.BytesIO()
							image.save(buffer, "png")
							buffer.seek(0)

							file = discord.File(buffer, filename="image.png")

							embed2.set_thumbnail(url="attachment://image.png")
							await msg.delete()
							msg2 = await message.channel.send(file=file,embed=embed2)
							return
						await msg.delete()
						msg2 = await message.channel.send(embed=embed2)
						return
					await msg.delete()
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorlink}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return
				try:
					cursor.execute(f"SELECT userid FROM users WHERE userid = {userprofile}")
				except:
					await msg.delete()
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorprofile}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return
				profile = cursor.fetchone()
				if profile is not None:
					usera = await message.guild.fetch_member(int(userprofile))
					if usera is None:
						await msg.delete()
						embed5 = discord.Embed(title="", color=0xff0000)
						embed5.add_field(name=f'{errormessage}', value=f"{errorprofile}")
						msg2 = await message.channel.send(embed=embed5)
						time.sleep(5)
						await msg2.delete()
						return
					try:
						iconprofile = usera.avatar_url
					except AttributeError:
						iconprofile = "https://cdn.discordapp.com/embed/avatars/0.png"
					if userprofile == jouca:
						owner = "<:owner:736727797191409694>"
					elif userprofile != jouca:
						owner = ""
					cursor.execute(f"SELECT userid FROM GDmoderators WHERE userid = {userprofile} LIMIT 1")
					try:
						mod = cursor.fetchone()[0]
					except TypeError:
						mod = None
					if mod is not None:
						cursor.execute(f"SELECT Modtype FROM GDmoderators WHERE userid = {userprofile} LIMIT 1")
						modtype = cursor.fetchone()[0]
						if modtype == "Mod":
							modbadge = "<:mod:472908845010780169>"
							eldermodbadge = ""
						elif modtype == "ElderMod":
							modbadge = ""
							eldermodbadge = "<:elder_mod:472907732538884117>"
					elif mod is None :
						modbadge = ""
						eldermodbadge = ""
					cursor.execute(f"SELECT userid FROM GRmoderators WHERE userid = {userprofile} LIMIT 1")
					try:
						modbot = cursor.fetchone()[0]
					except TypeError:
						modbot = None
					if modbot is not None:
						botmod = "<:GRmod:741965487096987739>"
					elif modbot is None:
						botmod = ""
					username = await client.fetch_user(int(userprofile))
					embed2 = discord.Embed(title=f"", color=0x696969)
					embed2.set_author(name=f"__{username}'s profile__", icon_url=(iconprofile))
					cursor.execute(f"SELECT levelrequestedcount,levelreviewedcount,levelreviewapprovedcount,levelreviewunapprovedcount FROM users WHERE userid = {userprofile}")
					datastats = cursor.fetchone()
					levelrequestedcount = datastats[0]
					levelreviewedcount = datastats[1]
					levelreviewapprovedcount = datastats[2]
					levelreviewunapprovedcount = datastats[3]
					cursor.execute(f"SELECT (SELECT COUNT(*) FROM users WHERE levelrequestedcount >= {levelrequestedcount}) AS position FROM users WHERE userid = {author}")
					levelrequestedcountposition = cursor.fetchone()[0]
					if levelrequestedcountposition == 1:
						levelrequestedcountposition = f"(<:top1:759751131114373161> #{levelrequestedcountposition})"
					elif levelrequestedcountposition >= 2 and levelrequestedcountposition <= 10:
						levelrequestedcountposition = f"(<:top10:759751146368925757> #{levelrequestedcountposition})"
					elif levelrequestedcountposition >= 11 and levelrequestedcountposition <= 50:
						levelrequestedcountposition = f"(<:top50:759751162860929054> #{levelrequestedcountposition})"
					elif levelrequestedcountposition >= 51 and levelrequestedcountposition <= 100:
						levelrequestedcountposition = f"(<:top100:759751174580338747> #{levelrequestedcountposition})"
					elif levelrequestedcountposition >= 101 and levelrequestedcountposition <= 500:
						levelrequestedcountposition = f"(<:top500:759751189192900649> #{levelrequestedcountposition})"
					elif levelrequestedcountposition >= 501 and levelrequestedcountposition <= 1000:
						levelrequestedcountposition = f"(<:top1000:759751201246937119> #{levelrequestedcountposition})"
					elif levelrequestedcountposition > 1000:
						levelrequestedcountposition = f"(<:topother:759751236819615765> #{levelrequestedcountposition})"
					cursor.execute(f"SELECT (SELECT COUNT(*) FROM users WHERE levelreviewedcount >= {levelreviewedcount}) AS position FROM users WHERE userid = {author}")
					levelreviewedcountposition = cursor.fetchone()[0]
					if levelreviewedcountposition == 1:
						levelreviewedcountposition = f"(<:top1:759751131114373161> #{levelreviewedcountposition})"
					elif levelreviewedcountposition >= 2 and levelreviewedcountposition <= 10:
						levelreviewedcountposition = f"(<:top10:759751146368925757> #{levelreviewedcountposition})"
					elif levelreviewedcountposition >= 11 and levelreviewedcountposition <= 50:
						levelreviewedcountposition = f"(<:top50:759751162860929054> #{levelreviewedcountposition})"
					elif levelreviewedcountposition >= 51 and levelreviewedcountposition <= 100:
						levelreviewedcountposition = f"(<:top100:759751174580338747> #{levelreviewedcountposition})"
					elif levelreviewedcountposition >= 101 and levelreviewedcountposition <= 500:
						levelreviewedcountposition = f"(<:top500:759751189192900649> #{levelreviewedcountposition})"
					elif levelreviewedcountposition >= 501 and levelreviewedcountposition <= 1000:
						levelreviewedcountposition = f"(<:top1000:759751201246937119> #{levelreviewedcountposition})"
					elif levelreviewedcountposition > 1000:
						levelreviewedcountposition = f"(<:topother:759751236819615765> #{levelreviewedcountposition})"
					cursor.execute(f"SELECT (SELECT COUNT(*) FROM users WHERE levelreviewapprovedcount >= {levelreviewapprovedcount}) AS position FROM users WHERE userid = {author}")
					levelreviewapprovedcountposition = cursor.fetchone()[0]
					if levelreviewapprovedcountposition == 1:
						levelreviewapprovedcountposition = f"(<:top1:759751131114373161> #{levelreviewapprovedcountposition})"
					elif levelreviewapprovedcountposition >= 2 and levelreviewapprovedcountposition <= 10:
						levelreviewapprovedcountposition = f"(<:top10:759751146368925757> #{levelreviewapprovedcountposition})"
					elif levelreviewapprovedcountposition >= 11 and levelreviewapprovedcountposition <= 50:
						levelreviewapprovedcountposition = f"(<:top50:759751162860929054> #{levelreviewapprovedcountposition})"
					elif levelreviewapprovedcountposition >= 51 and levelreviewapprovedcountposition <= 100:
						levelreviewapprovedcountposition = f"(<:top100:759751174580338747> #{levelreviewapprovedcountposition})"
					elif levelreviewapprovedcountposition >= 101 and levelreviewapprovedcountposition <= 500:
						levelreviewapprovedcountposition = f"(<:top500:759751189192900649> #{levelreviewapprovedcountposition})"
					elif levelreviewapprovedcountposition >= 501 and levelreviewapprovedcountposition <= 1000:
						levelreviewapprovedcountposition = f"(<:top1000:759751201246937119> #{levelreviewapprovedcountposition})"
					elif levelreviewapprovedcountposition > 1000:
						levelreviewapprovedcountposition = f"_(<:topother:759751236819615765> #{levelreviewapprovedcountposition})"
					cursor.execute(f"SELECT (SELECT COUNT(*) FROM users WHERE levelreviewunapprovedcount >= {levelreviewunapprovedcount}) AS position FROM users WHERE userid = {author}")
					levelreviewunapprovedcountposition = cursor.fetchone()[0]
					if levelreviewunapprovedcountposition == 1:
						levelreviewunapprovedcountposition = f"(<:top1:759751131114373161> #{levelreviewunapprovedcountposition})"
					elif levelreviewunapprovedcountposition >= 2 and levelreviewunapprovedcountposition <= 10:
						levelreviewunapprovedcountposition = f"(<:top10:759751146368925757> #{levelreviewunapprovedcountposition})"
					elif levelreviewunapprovedcountposition >= 11 and levelreviewunapprovedcountposition <= 50:
						levelreviewunapprovedcountposition = f"(<:top50:759751162860929054> #{levelreviewunapprovedcountposition})"
					elif levelreviewunapprovedcountposition >= 51 and levelreviewunapprovedcountposition <= 100:
						levelreviewunapprovedcountposition = f"(<:top100:759751174580338747> #{levelreviewunapprovedcountposition})"
					elif levelreviewunapprovedcountposition >= 101 and levelreviewunapprovedcountposition <= 500:
						levelreviewunapprovedcountposition = f"(<:top500:759751189192900649> #{levelreviewunapprovedcountposition})"
					elif levelreviewunapprovedcountposition >= 501 and levelreviewunapprovedcountposition <= 1000:
						levelreviewunapprovedcountposition = f"(<:top1000:759751201246937119> #{levelreviewunapprovedcountposition})"
					elif levelreviewunapprovedcountposition > 1000:
						levelreviewunapprovedcountposition = f"(<:topother:759751236819615765> #{levelreviewunapprovedcountposition})"
					embed2.add_field(name=f'{owner}{botmod}{eldermodbadge}{modbadge} {username}', value=f"<:requests:726371180508086283> Levels Requested : `{levelrequestedcount}` {levelrequestedcountposition}\n<:reviewed:726371160589205524> Levels Reviewed : `{levelreviewedcount}` {levelreviewedcountposition}\n<:approved:726371180075810816> Levels Approved : `{levelreviewapprovedcount}` {levelreviewapprovedcountposition}\n<:unapproved:726371181875429406> Levels Unapproved : `{levelreviewunapprovedcount}` {levelreviewunapprovedcountposition}", inline=False)
					if userprofile == jouca:
						ownertext = "<:owner:736727797191409694> OWNER\n"
					elif userprofile != jouca:
						ownertext = ""
					if modbot is not None:
						modbottext = "<:GRmod:741965487096987739> GEOMETRY REQUESTS MODERATOR\n"
					elif modbot is None:
						modbottext = ""
					if mod is not None:
						if modtype == "Mod":
							modtext = "<:mod:472908845010780169> GD MODERATOR"
						elif modtype == "ElderMod":
							modtext = "<:elder_mod:472907732538884117> GD ELDER MODERATOR"
					elif mod is None:
						modtext = ""
					ranks = f"{ownertext}{modbottext}{modtext}"
					embed2.add_field(name=f'───────────', value=f"**{ranks}\n<:discord:472907660065505300> Discord : {username}**", inline=False)
					embed2.add_field(name=f'───────────', value=f"_For settings, use `req!settings profile`_", inline=False)
					cursor.execute(f"SELECT ID FROM users WHERE userid = {userprofile}")
					accountid = cursor.fetchone()[0]
					embed2.set_footer(text=f"AccountID : {accountid}")

					cursor.execute(f"SELECT isCubeUnlocked FROM users WHERE userid = {userprofile}")
					iscubeunlocked = cursor.fetchone()[0]
					if iscubeunlocked == 1:
						cursor.execute(f"SELECT cubetype FROM users WHERE userid = {userprofile}")
						icontypeid = cursor.fetchone()[0]
						cursor.execute(f"SELECT color1,color2 FROM users WHERE userid = {userprofile}")
						icons = cursor.fetchone()
						color1 = int(icons[0],base=16)
						color2 = int(icons[1],base=16)
						cursor.execute(f"SELECT glowoutline FROM users WHERE userid = {userprofile}")
						glowoutline = cursor.fetchone()[0]
						if glowoutline == 0:
							glowoutline = False
						elif glowoutline == 1:
							glowoutline = True
						image = gd.factory.generate(icon_type="cube", icon_id=int(icontypeid), color_1=gd.Color(color1), color_2=gd.Color(color2), glow_outline=glowoutline)
						buffer = io.BytesIO()
						image.save(buffer, "png")
						buffer.seek(0)

						file = discord.File(buffer, filename="image.png")

						embed2.set_thumbnail(url="attachment://image.png")
						await msg.delete()
						msg2 = await message.channel.send(file=file,embed=embed2)
						return
					await msg.delete()
					msg2 = await message.channel.send(embed=embed2)
					return
				await msg.delete()
				embed5 = discord.Embed(title="", color=0xff0000)
				embed5.add_field(name=f'{errormessage}', value=f"{errorprofile}")
				msg2 = await message.channel.send(embed=embed5)
				time.sleep(5)
				await msg2.delete()
				return

		if msg.startswith("settings profile"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor()

				maincommand = "reqsettingsprofile"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				args = [x for ar in args for x in ar.split('\n')]
				
				server = message.guild.name
				var = message.guild.id
				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqsettings profile/{language2}.txt").read().splitlines()

				errormessage = translate_messages[0]
				errorlink = translate_messages[1]

				profiletitle = translate_messages[3]
				information = translate_messages[4]
				informationdesc = translate_messages[5]

				languagetitle = translate_messages[7]
				englishlanguage = translate_messages[8]
				frenchlanguage = translate_messages[9]
				spanishlanguage = translate_messages[10]

				documentation = translate_messages[12]

				cursor.execute(f"SELECT * FROM users WHERE userid = {author} LIMIT 1")
				result = cursor.fetchone()
				if result is not None:
					embed = discord.Embed(title=f"{profiletitle}", color=0x8E8E8E)
					usera = await message.guild.fetch_member(author)
					iconprofile = usera.avatar_url
					embed.set_author(name=f"__{message.author}__", icon_url=(iconprofile))
					languagesetup = result[31]
					if languagesetup == "en":
						embed.add_field(name=f"{languagetitle}", value=f"{englishlanguage}", inline=False)
					elif languagesetup == "fr":
						embed.add_field(name=f"{languagetitle}", value=f"{frenchlanguage}", inline=False)
					elif languagesetup == "es":
						embed.add_field(name=f"{languagetitle}", value=f"{spanishlanguage}", inline=False)
					embed.add_field(name=f"{information}", value=f"{informationdesc}", inline=False)

					cursor.execute(f"SELECT isCubeUnlocked FROM users WHERE userid = {author}")
					iscubeunlocked = cursor.fetchone()[0]
					if iscubeunlocked == 1:
						cubetypetitle = result[33]
						color1title = result[34]
						color2title = result[35]
						glowoutlinetitle = result[36]
						embed.add_field(name=f"CubeID", value=f"{cubetypetitle}", inline=False)
						embed.add_field(name=f"Color1", value=f"{color1title}", inline=False)
						embed.add_field(name=f"Color2", value=f"{color2title}", inline=False)
						embed.add_field(name=f"GlowOutline", value=f"{glowoutlinetitle}", inline=False)
						embed.add_field(name=f"{documentation}", value=f"[Geometry Requests Icons/Colors Documentation](https://docs.google.com/document/d/17jI3LPAkutHaLwwpLdpCBfivRCCvM_OuboVavx7n84g/edit?usp=sharing)", inline=False)
						cursor.execute(f"SELECT cubetype FROM users WHERE userid = {author}")
						icontypeid = cursor.fetchone()[0]
						cursor.execute(f"SELECT color1,color2 FROM users WHERE userid = {author}")
						icons = cursor.fetchone()
						color1 = int(icons[0],base=16)
						color2 = int(icons[1],base=16)
						cursor.execute(f"SELECT glowoutline FROM users WHERE userid = {author}")
						glowoutline = cursor.fetchone()[0]
						if glowoutline == 0:
							glowoutline = False
						elif glowoutline == 1:
							glowoutline = True
						image = gd.factory.generate(icon_type="cube", icon_id=int(icontypeid), color_1=gd.Color(color1), color_2=gd.Color(color2), glow_outline=glowoutline)
						buffer = io.BytesIO()
						image.save(buffer, "png")
						buffer.seek(0)

						file = discord.File(buffer, filename="image.png")

						embed.set_thumbnail(url="attachment://image.png")
						embed.set_footer(text=f"{message.guild.name} --- {message.author}")
						msg = await message.channel.send(file=file,embed=embed)
						return
					embed.set_footer(text=f"{message.guild.name} --- {message.author}")
					msg = await message.channel.send(embed=embed)
					return
				else:
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorlink}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return

		if msg.startswith("setsettings profile"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor()

				maincommand = "reqsetsettingsprofile"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				args = [x for ar in args for x in ar.split('\n')]
				
				try:
					description = args[2]
				except IndexError as error:
					description = None
				try:
					valeur = args[3]
				except IndexError as error:
					valeur = 0
				server = message.guild.name
				var = message.guild.id
				author = message.author.id
				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqsetsettings profile/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				errorlink = translate_messages[4]
				errorlanguage = translate_messages[5]
				errorsetting = translate_messages[6]

				successtitle = translate_messages[8]
				successdesc = translate_messages[9]

				errorcolor = translate_messages[11]
				erroricon = translate_messages[12]
				errorbinary = translate_messages[13]

				cursor.execute(f"SELECT userid FROM users WHERE userid = {author}")
				linked = cursor.fetchone()
				if linked is None:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorlink}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				if description is not None:
					if description == "language":
						if valeur == "en":
							var = message.guild.id
							embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
							embed3.add_field(name=f"{loadingdesc}", value="\u200b")
							msg = await message.channel.send(embed=embed3)
							cursor.execute(f"UPDATE users SET language = 'en' WHERE userid = {author}")
							conn.commit()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f'{successdesc}', value='\u200b')
							await msg.delete()
							msg = await message.channel.send(embed=embed)
							return
						elif valeur == "fr":
							var = message.guild.id
							embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
							embed3.add_field(name=f"{loadingdesc}", value="\u200b")
							msg = await message.channel.send(embed=embed3)
							cursor.execute(f"UPDATE users SET language = 'fr' WHERE userid = {author}")
							conn.commit()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f'{successdesc}', value='\u200b')
							await msg.delete()
							msg = await message.channel.send(embed=embed)
							return
						elif valeur == "es":
							var = message.guild.id
							embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
							embed3.add_field(name=f"{loadingdesc}", value="\u200b")
							msg = await message.channel.send(embed=embed3)
							cursor.execute(f"UPDATE users SET language = 'es' WHERE userid = {author}")
							conn.commit()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f'{successdesc}', value='\u200b')
							await msg.delete()
							msg = await message.channel.send(embed=embed)
							return
						else:
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorlanguage}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
					elif description == "color1":
						for color in color_palette:
							if valeur.endswith(color):
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE users SET color1 = '{valeur}' WHERE userid = {author}")
								conn.commit()
								embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
								embed.add_field(name=f'{successdesc}', value='\u200b')
								await msg.delete()
								msg = await message.channel.send(embed=embed)
								return
							else:
								pass
						else:
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorcolor}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
					elif description == "color2":
						for color in color_palette:
							if valeur.endswith(color):
								embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed3.add_field(name=f"{loadingdesc}", value="\u200b")
								msg = await message.channel.send(embed=embed3)
								cursor.execute(f"UPDATE users SET color2 = '{valeur}' WHERE userid = {author}")
								conn.commit()
								embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
								embed.add_field(name=f'{successdesc}', value='\u200b')
								await msg.delete()
								msg = await message.channel.send(embed=embed)
								return
							else:
								pass
						else:
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorcolor}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
					elif description == "cubeid":
						valeur = int(valeur)
						if valeur >= 1 and valeur <= 142:
							embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
							embed3.add_field(name=f"{loadingdesc}", value="\u200b")
							msg = await message.channel.send(embed=embed3)
							cursor.execute(f"UPDATE users SET cubetype = '{valeur}' WHERE userid = {author}")
							conn.commit()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f'{successdesc}', value='\u200b')
							await msg.delete()
							msg = await message.channel.send(embed=embed)
							return
						else:
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{erroricon}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
					elif description == "glowoutline":
						if valeur == "0" or valeur == "1":
							valeur = int(valeur)
							embed3 = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
							embed3.add_field(name=f"{loadingdesc}", value="\u200b")
							msg = await message.channel.send(embed=embed3)
							cursor.execute(f"UPDATE users SET glowoutline = '{valeur}' WHERE userid = {author}")
							conn.commit()
							embed = discord.Embed(title=f'{successtitle}', color=0x00ff00)
							embed.add_field(name=f'{successdesc}', value='\u200b')
							await msg.delete()
							msg = await message.channel.send(embed=embed)
							return
						else:
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorbinary}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
					else:
						embed = discord.Embed(title="", color=0xff0000)
						embed.add_field(name=f'{errormessage}', value=f"{errorsetting}")
						msg2 = await message.channel.send(embed=embed)
						time.sleep(5)
						await msg2.delete()
						return
				else:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorsetting}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

		if msg.startswith("leaderboard"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor()
				server = message.guild.name
				var = message.guild.id
				author = message.author.id

				maincommand = "reqleaderboard"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				
				if author != jouca:
					return
				try:
					typeleaderboard = args[1]
				except IndexError as error:
					typeleaderboard = "requests"

				cursor.execute(f"SELECT language FROM users WHERE userid = {author}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default

				language2 = language
				translate_messages = open(f"language/client/reqleaderboard/{language2}.txt").read().splitlines()
				
				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]
				
				information = translate_messages[3]
				page = translate_messages[4]
				reactions = translate_messages[5]
				
				top100requests = translate_messages[7]
				top100reviews = translate_messages[8]
				top100approved = translate_messages[9]
				top100unapproved = translate_messages[10]
				
				embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
				embed.add_field(name=f'{loadingdesc}', value="\u200b")
				msg = await message.channel.send(embed=embed)
				if typeleaderboard == "requests":
					cursor.execute("SELECT userid FROM users ORDER BY levelrequestedcount DESC LIMIT 100")
					userslist = cursor.fetchall()
					userslist = [x[0] for x in userslist]
					listplace = []
					
					for i in range(0,20):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete1 = "".join(listplace)
					embed1 = discord.Embed(title=f"<:requests:726371180508086283> {top100requests}",description=f"{listcomplete1}",color=0xfeff00)
					embed1.add_field(name=f"{information}", value=f"{page} 1/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(20,40):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete2 = "".join(listplace)
					embed2 = discord.Embed(title=f"<:requests:726371180508086283> {top100requests}",description=f"{listcomplete2}",color=0xfeff00)
					embed2.add_field(name=f"{information}", value=f"{page} 2/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(40,60):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete3 = "".join(listplace)
					embed3 = discord.Embed(title=f"<:requests:726371180508086283> {top100requests}",description=f"{listcomplete3}",color=0xfeff00)
					embed3.add_field(name=f"{information}", value=f"{page} 3/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(60,80):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete4 = "".join(listplace)
					embed4 = discord.Embed(title=f"<:requests:726371180508086283> {top100requests}",description=f"{listcomplete4}",color=0xfeff00)
					embed4.add_field(name=f"{information}", value=f"{page} 4/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(80,100):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete5 = "".join(listplace)
					embed5 = discord.Embed(title=f"<:requests:726371180508086283> {top100requests}",description=f"{listcomplete5}",color=0xfeff00)
					embed5.add_field(name=f"{information}", value=f"{page} 5/5 - {reactions}", inline=False)
					
					await msg.delete()
					messages = (embed1,embed2,embed3,embed4,embed5)
					index = 0
					msg = None
					action = message.channel.send
					while True:
						res = await action(embed=messages[index])
						if res is not None:
							msg = res
						l = index != 0
						r = index != len(messages) - 1
						if l:
							await msg.add_reaction(left)
						if r:
							await msg.add_reaction(right)
						try:
							react, user = await client.wait_for('reaction_add', check=predicate(msg, l, r), timeout=30)
						except Exception:
							print("BROKE")
							break
						if react.emoji == left:
							index -= 1
						elif react.emoji == right:
							index += 1
						action = msg.edit					
					return
				elif typeleaderboard == "reviews":
					cursor.execute("SELECT userid FROM users ORDER BY levelreviewedcount DESC LIMIT 100")
					userslist = cursor.fetchall()
					userslist = [x[0] for x in userslist]
					listplace = []
					
					for i in range(0,20):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete1 = "".join(listplace)
					embed1 = discord.Embed(title=f"<:reviewed:726371160589205524> {top100reviews}",description=f"{listcomplete1}",color=0xfeff00)
					embed1.add_field(name=f"{information}", value=f"{page} 1/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(20,40):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete2 = "".join(listplace)
					embed2 = discord.Embed(title=f"<:reviewed:726371160589205524> {top100reviews}",description=f"{listcomplete2}",color=0xfeff00)
					embed2.add_field(name=f"{information}", value=f"{page} 2/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(40,60):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete3 = "".join(listplace)
					embed3 = discord.Embed(title=f"<:reviewed:726371160589205524> {top100reviews}",description=f"{listcomplete3}",color=0xfeff00)
					embed3.add_field(name=f"{information}", value=f"{page} 3/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(60,80):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete4 = "".join(listplace)
					embed4 = discord.Embed(title=f"<:reviewed:726371160589205524> {top100reviews}",description=f"{listcomplete4}",color=0xfeff00)
					embed4.add_field(name=f"{information}", value=f"{page} 4/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(80,100):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete5 = "".join(listplace)
					embed5 = discord.Embed(title=f"<:reviewed:726371160589205524> {top100reviews}",description=f"{listcomplete5}",color=0xfeff00)
					embed5.add_field(name=f"{information}", value=f"{page} 5/5 - {reactions}", inline=False)
					
					await msg.delete()
					messages = (embed1,embed2,embed3,embed4,embed5)
					index = 0
					msg = None
					action = message.channel.send
					while True:
						res = await action(embed=messages[index])
						if res is not None:
							msg = res
						l = index != 0
						r = index != len(messages) - 1
						if l:
							await msg.add_reaction(left)
						if r:
							await msg.add_reaction(right)
						try:
							react, user = await client.wait_for('reaction_add', check=predicate(msg, l, r), timeout=30)
						except Exception:
							print("BROKE")
							break
						if react.emoji == left:
							index -= 1
						elif react.emoji == right:
							index += 1
						action = msg.edit					
					return
				elif typeleaderboard == "reviewsapproved":
					cursor.execute("SELECT userid FROM users ORDER BY levelreviewapprovedcount DESC LIMIT 100")
					userslist = cursor.fetchall()
					userslist = [x[0] for x in userslist]
					listplace = []
					
					for i in range(0,20):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete1 = "".join(listplace)
					embed1 = discord.Embed(title=f"<:approved:726371180075810816> {top100approved}",description=f"{listcomplete1}",color=0xfeff00)
					embed1.add_field(name=f"{information}", value=f"{page} 1/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(20,40):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete2 = "".join(listplace)
					embed2 = discord.Embed(title=f"<:approved:726371180075810816> {top100approved}",description=f"{listcomplete2}",color=0xfeff00)
					embed2.add_field(name=f"{information}", value=f"{page} 2/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(40,60):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete3 = "".join(listplace)
					embed3 = discord.Embed(title=f"<:approved:726371180075810816> {top100approved}",description=f"{listcomplete3}",color=0xfeff00)
					embed3.add_field(name=f"{information}", value=f"{page} 3/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(60,80):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete4 = "".join(listplace)
					embed4 = discord.Embed(title=f"<:approved:726371180075810816> {top100approved}",description=f"{listcomplete4}",color=0xfeff00)
					embed4.add_field(name=f"{information}", value=f"{page} 4/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(80,100):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete5 = "".join(listplace)
					embed5 = discord.Embed(title=f"<:approved:726371180075810816> {top100approved}",description=f"{listcomplete5}",color=0xfeff00)
					embed5.add_field(name=f"{information}", value=f"{page} 5/5 - {reactions}", inline=False)
					
					await msg.delete()
					messages = (embed1,embed2,embed3,embed4,embed5)
					index = 0
					msg = None
					action = message.channel.send
					while True:
						res = await action(embed=messages[index])
						if res is not None:
							msg = res
						l = index != 0
						r = index != len(messages) - 1
						if l:
							await msg.add_reaction(left)
						if r:
							await msg.add_reaction(right)
						try:
							react, user = await client.wait_for('reaction_add', check=predicate(msg, l, r), timeout=30)
						except Exception:
							print("BROKE")
							break
						if react.emoji == left:
							index -= 1
						elif react.emoji == right:
							index += 1
						action = msg.edit					
					return
				elif typeleaderboard == "reviewsunapproved":
					cursor.execute("SELECT userid FROM users ORDER BY levelreviewunapprovedcount DESC LIMIT 100")
					userslist = cursor.fetchall()
					userslist = [x[0] for x in userslist]
					listplace = []
					
					for i in range(0,20):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete1 = "".join(listplace)
					embed1 = discord.Embed(title=f"<:unapproved:726371181875429406> {top100unapproved}",description=f"{listcomplete1}",color=0xfeff00)
					embed1.add_field(name=f"{information}", value=f"{page} 1/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(20,40):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete2 = "".join(listplace)
					embed2 = discord.Embed(title=f"<:unapproved:726371181875429406> {top100unapproved}",description=f"{listcomplete2}",color=0xfeff00)
					embed2.add_field(name=f"{information}", value=f"{page} 2/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(40,60):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete3 = "".join(listplace)
					embed3 = discord.Embed(title=f"<:unapproved:726371181875429406> {top100unapproved}",description=f"{listcomplete3}",color=0xfeff00)
					embed3.add_field(name=f"{information}", value=f"{page} 3/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(60,80):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete4 = "".join(listplace)
					embed4 = discord.Embed(title=f"<:unapproved:726371181875429406> {top100unapproved}",description=f"{listcomplete4}",color=0xfeff00)
					embed4.add_field(name=f"{information}", value=f"{page} 4/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(80,100):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete5 = "".join(listplace)
					embed5 = discord.Embed(title=f"<:unapproved:726371181875429406> {top100unapproved}",description=f"{listcomplete5}",color=0xfeff00)
					embed5.add_field(name=f"{information}", value=f"{page} 5/5 - {reactions}", inline=False)
					
					await msg.delete()
					messages = (embed1,embed2,embed3,embed4,embed5)
					index = 0
					msg = None
					action = message.channel.send
					while True:
						res = await action(embed=messages[index])
						if res is not None:
							msg = res
						l = index != 0
						r = index != len(messages) - 1
						if l:
							await msg.add_reaction(left)
						if r:
							await msg.add_reaction(right)
						try:
							react, user = await client.wait_for('reaction_add', check=predicate(msg, l, r), timeout=30)
						except Exception:
							print("BROKE")
							break
						if react.emoji == left:
							index -= 1
						elif react.emoji == right:
							index += 1
						action = msg.edit					
					return
				else:
					cursor.execute("SELECT userid FROM users ORDER BY levelrequestedcount DESC LIMIT 100")
					userslist = cursor.fetchall()
					userslist = [x[0] for x in userslist]
					listplace = []
					
					for i in range(0,20):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete1 = "".join(listplace)
					embed1 = discord.Embed(title=f"<:requests:726371180508086283> {top100requests}",description=f"{listcomplete1}",color=0xfeff00)
					embed1.add_field(name=f"{information}", value=f"{page} 1/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(20,40):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete2 = "".join(listplace)
					embed2 = discord.Embed(title=f"<:requests:726371180508086283> {top100requests}",description=f"{listcomplete2}",color=0xfeff00)
					embed2.add_field(name=f"{information}", value=f"{page} 2/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(40,60):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete3 = "".join(listplace)
					embed3 = discord.Embed(title=f"<:requests:726371180508086283> {top100requests}",description=f"{listcomplete3}",color=0xfeff00)
					embed3.add_field(name=f"{information}", value=f"{page} 3/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(60,80):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete4 = "".join(listplace)
					embed4 = discord.Embed(title=f"<:requests:726371180508086283> {top100requests}",description=f"{listcomplete4}",color=0xfeff00)
					embed4.add_field(name=f"{information}", value=f"{page} 4/5 - {reactions}", inline=False)
					
					listplace = []
					for i in range(80,100):
						userprofile = userslist[i]
						username = await client.fetch_user(int(userprofile))
						place = i+1
						if i == 0:
							leaderboardtext = f"<:top1:759751131114373161>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 1 and i <= 9:
							leaderboardtext = f"<:top10:759751146368925757>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 10 and i <= 49:
							leaderboardtext = f"<:top50:759751162860929054>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
						elif i >= 50 and i <= 99:
							leaderboardtext = f"<:top100:759751174580338747>**#{place}** - {username}\n"
							listplace.append(leaderboardtext)
					listcomplete5 = "".join(listplace)
					embed5 = discord.Embed(title=f"<:requests:726371180508086283> {top100requests}",description=f"{listcomplete5}",color=0xfeff00)
					embed5.add_field(name=f"{information}", value=f"{page} 5/5 - {reactions}", inline=False)
					
					await msg.delete()
					messages = (embed1,embed2,embed3,embed4,embed5)
					index = 0
					msg = None
					action = message.channel.send
					while True:
						res = await action(embed=messages[index])
						if res is not None:
							msg = res
						l = index != 0
						r = index != len(messages) - 1
						if l:
							await msg.add_reaction(left)
						if r:
							await msg.add_reaction(right)
						try:
							react, user = await client.wait_for('reaction_add', check=predicate(msg, l, r), timeout=30)
						except Exception:
							print("BROKE")
							break
						if react.emoji == left:
							index -= 1
						elif react.emoji == right:
							index += 1
						action = msg.edit					
					return
				
		'''if msg.startswith("token"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor()
				tokenurl = secrets.token_urlsafe(10)
				author = message.author.id
				ts = time.time()
				timestamp = int(ts) + 86400
				timern = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
				sql = "INSERT INTO tokens (token, client, timestamp, chesttype) VALUES (%s, %s, %s, %s)"
				var = (tokenurl,author,timern,1)
				cursor.execute(sql, var)
				conn.commit()
				return

		if msg.startswith("demonroulette"):
			return'''

		if msg.startswith("remove"):
			serverid = message.guild.id
			author = message.author.id
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				authorid = message.author.id
				serverid = message.guild.id

				maincommand = "reqremove"
				checkmaintenance = checkmaintenance(maincommand)
				if checkmaintenance == "yes":
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'Error. <:error:472907618386575370>', value=f"**The command is under maintenance, please try again later.**")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return

				cursor.execute(f"SELECT language FROM users WHERE userid = {authorid}")
				try:
					language = cursor.fetchone()[0]
				except TypeError:
					language = language_default
				language2 = language
				translate_messages = open(f"language/client/reqremove/{language2}.txt").read().splitlines()

				loadingtitle = translate_messages[0]
				loadingdesc = translate_messages[1]

				errormessage = translate_messages[3]
				erroridnotfound1 = translate_messages[4]
				erroridnotfound2 = translate_messages[5]
				errorallsyntax = translate_messages[6]
				errorlevelid = translate_messages[7]
				errorpermission = translate_messages[8]

				completed = translate_messages[10]
				levelscompleted = translate_messages[11]
				levelcompleted = translate_messages[12]
				
				translate_cooldown_messages = open(f"language/client/cooldown-{language2}.txt").read().splitlines()
				errorcooldown1 = translate_cooldown_messages[0]
				errorcooldown2 = translate_cooldown_messages[1]
				
				#cooldowncheck(author)
				alwayscooldown,secondcooldown = cooldowncheck(author)
				
				if alwayscooldown == 1:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name=f'{errormessage}', value=f"{errorcooldown1} {secondcooldown} {errorcooldown2}")
					msg2 = await message.channel.send(embed=embed)
					time.sleep(5)
					await msg2.delete()
					return
				sql = "INSERT INTO cooldowns (userid, cooldown) VALUES (%s, %s)"
				datetime_object_cooldown = datetime_object + datetime.timedelta(seconds=30)
				val = (author, datetime_object_cooldown)
				cursor.execute(sql,val)
				conn.commit()

				try:
					level = args[1]
				except IndexError:
					level = None
				if message.author.guild_permissions.administrator:
					if level is not None:
						conn.cursor()
						if level == "all":
							embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
							embed.add_field(name=f'{loadingdesc}', value="\u200b")
							msg = await message.channel.send(embed=embed)

							cursor.execute(f"SELECT levelid FROM levels WHERE server = {serverid}")
							levels = cursor.fetchall()
							for i in levels:
								cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
								channelmessageid = cursor.fetchone()[0]
								channelmessageid = client.get_channel(int(channelmessageid))

								cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {i[0]}")
								messages = cursor.fetchone()[0]
								try:
									msg101 = await channelmessageid.fetch_message(int(messages))
									await msg101.delete()
								except:
									cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
									channelmessageid = cursor.fetchone()[0]
									channelmessageid = client.get_channel(int(channelmessageid))
									try:
										msg101 = await channelmessageid.fetch_message(int(messages))
										await msg101.delete()
									except:
										pass

							cursor.execute(f"DELETE FROM levels WHERE server = {serverid}")
							conn.commit()
							await asyncio.sleep(3)
							await msg.delete()

							embed = discord.Embed(title="", color=0x00ff00)
							embed.add_field(name=f'{completed}', value=f'{levelscompleted}')
							embed.set_footer(text=f"{message.guild.name} --- {message.author}")
							msg2 = await message.channel.send(embed=embed)
							return
						data = f"gameVersion=21&binaryVersion=35&gdw=0&type=0&str={level}&diff=-&len=-&page=0&total=0&secret=Wmfd2893gb7".encode()
						result = urlopen("http://www.boomlings.com/database/getGJLevels21.php",data).read().decode()
						if result == "-1":
							embed = discord.Embed(title="", color=0xff0000)
							embed.add_field(name=f'{errormessage}', value=f"{errorlevelid}")
							msg2 = await message.channel.send(embed=embed)
							time.sleep(5)
							await msg2.delete()
							return
						pogga = cursor.execute(f"SELECT levelid FROM levels WHERE server = {serverid} AND levelid = %s", (level, ))
						try:
							number = cursor.fetchone()[0]
						except TypeError:
							number = None
						else:
							if str(number) == level:
								embed = discord.Embed(title=f"{loadingtitle}", color=0xffce08)
								embed.add_field(name=f'{loadingdesc}', value="\u200b")
								msg = await message.channel.send(embed=embed)
								
								cursor.execute(f"SELECT ReviewChannel FROM setup WHERE serverid = {serverid}")
								channelmessageid = cursor.fetchone()[0]
								channelmessageid = client.get_channel(int(channelmessageid))

								cursor.execute(f"SELECT messageid FROM levels WHERE server = {serverid} AND levelid = {level}")
								messages = cursor.fetchone()[0]
								try:
									msg101 = await channelmessageid.fetch_message(int(messages))
									await msg101.delete()
								except:
									cursor.execute(f"SELECT GDModChannel FROM setup WHERE serverid = {serverid}")
									channelmessageid = cursor.fetchone()[0]
									channelmessageid = client.get_channel(int(channelmessageid))
									try:
										msg101 = await channelmessageid.fetch_message(int(messages))
										await msg101.delete()
									except:
										pass

								cursor.execute(f"DELETE FROM levels WHERE server = {serverid} AND levelid = %s", (level, ))
								conn.commit()
								await asyncio.sleep(3)
								await msg.delete()

								embed = discord.Embed(title="", color=0x00ff00)
								embed.add_field(name=f'{completed}', value=f'{levelcompleted}')
								embed.set_footer(text=f"{message.guild.name} --- {message.author}")
								msg2 = await message.channel.send(embed=embed)
								return
							if number is None:
								embed5 = discord.Embed(title="", color=0xff0000)
								embed5.add_field(name=f'{errormessage}', value=f"{erroridnotfound1} `{level}` {erroridnotfound2}")
								msg2 = await message.channel.send(embed=embed5)
								time.sleep(5)
								await msg2.delete()
								return
							else:
								embed5 = discord.Embed(title="", color=0xff0000)
								embed5.add_field(name=f'{errormessage}', value=f"{errorallsyntax}")
								msg2 = await message.channel.send(embed=embed5)
								time.sleep(5)
								await msg2.delete()
								return
					else:
						embed5 = discord.Embed(title="", color=0xff0000)
						embed5.add_field(name=f'{errormessage}', value=f"{errorlevelid}")
						msg2 = await message.channel.send(embed=embed5)
						time.sleep(5)
						await msg2.delete()
						return
				else:
					embed5 = discord.Embed(title="", color=0xff0000)
					embed5.add_field(name=f'{errormessage}', value=f"{errorpermission}")
					msg2 = await message.channel.send(embed=embed5)
					time.sleep(5)
					await msg2.delete()
					return

	except Exception as error:
		args2 = prefix,' '.join(args)
		msg404 = traceback.format_exc()
		channel2 = client.get_channel(int(718454176803192834))
		embed = discord.Embed(title="", color=0xff0000)
		embed.add_field(name='An error occured with the bot. <:error:472907618386575370>', value=f"Input :```{args2}```Output :```{msg404}```Please make sure to retry multiple times to see if the error is the same.\nif it's the same, report this bug on the Official Discord server of Geometry Request on the channel #report-bugs (link of the official discord in the command 'req!help').")
		embed.set_footer(text=f"{message.guild.name} --- {message.author}")
		embed2 = discord.Embed(title="", color=0xff0000)
		embed2.add_field(name='An error occured with the bot. <:error:472907618386575370>', value=f'Input :```{args2}```Output :```{msg404}```')
		embed2.set_footer(text=f"{message.guild.name} --- {message.author}")
		await message.channel.send(embed=embed)
		await channel2.send("<@&717133903328182392>",embed=embed2)
		return

@client.event
async def on_guild_join(guild):
	try:
		conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
		cursor = conn.cursor()
	except MC.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is not right with your username or your password")
			return
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
			return
		else:
			print(err)
			return
	else:
		conn.cursor(buffered=True)
		default = None
		zero = 0
		bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).flatten()
		serverid = guild.id
		servername = guild.name
		conn.cursor()
		sql = "INSERT INTO setup (serverid, ReviewerRole, OwnerRole, RequestChannel, ReviewChannel, CheckedReviewChannel, AnnouncementBot, GDModChannel, TagReviewer, NeedVideo, language, RemoveRated, GDModCheckedChannel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		var = (serverid,default,default,default,default,default,default,default,zero,zero,"en",zero,default)
		cursor.execute(sql, var)
		embed = discord.Embed(title="", color=0x00ff00)
		embed.add_field(name='Thanks for adding me! <:success:472908961176092702>', value='Hello, thank you for adding me on your server ! Before starting the tutorial, I would like to tell you that this bot is completely unrelated to Geometry Dash (except on searchs). So, this robot will in no case request your identifiers or a means of using your GD account. Now, to start using the bot you need to type the command `req!help` for see every commands (i recomment you after to setup your discord with the commands too).')
		try:
			msg300 = await bot_entry[0].user.send(embed=embed)
		except discord.errors:
			pass
		await client.change_presence(activity=discord.Streaming(name="req!help | In "+str(len(client.guilds))+" servers!", url="https://www.twitch.tv/joucayt"))
		channel2 = client.get_channel(int(719566509264863282))
		await channel2.send(f"<:success:472908961176092702> - Bot have been added on `{servername}`")

		conn.commit()

@client.event
async def on_guild_remove(guild):
	try:
		conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
		cursor = conn.cursor()
	except MC.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is not right with your username or your password")
			return
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
			return
		else:
			print(err)
			return
	else:
		conn.cursor(buffered=True)
		serverid = guild.id
		servername = guild.name
		conn.cursor()
		cursor.execute(f"DELETE FROM setup WHERE serverid = {serverid}")
		conn.commit()
		cursor.execute(f"DELETE FROM levels WHERE server = {serverid}")
		await client.change_presence(activity=discord.Streaming(name="req!help | In "+str(len(client.guilds))+" servers!", url="https://www.twitch.tv/joucayt"))
		conn.commit()
		channel2 = client.get_channel(int(719566509264863282))
		await channel2.send(f"<:error:472907618386575370> - Bot have been removed on `{servername}`")

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await client.change_presence(activity=discord.Streaming(name="req!help | In "+str(len(client.guilds))+" servers!", url="https://www.twitch.tv/joucayt"))
	datetime_object = datetime.datetime.now()
	channellog = client.get_channel(int(765611422389633064))
	await channellog.send(f"<:granted:718913909905424474> **[{datetime_object}]** Bot is ready !")

client.run(TOKEN)
