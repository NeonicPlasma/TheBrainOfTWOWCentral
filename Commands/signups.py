import discord, datetime
from Config._db import Database

def HELP(PREFIX):
	return {
		"COOLDOWN": 2,
		"MAIN": "Command to manage the #twows-in-signups channel",
		"FORMAT": "wip",
		"CHANNEL": 0,
		"USAGE": f"""wip""".replace("\n", "").replace("\t", "")
	}

PERMS = 2 # Staff
ALIASES = [""]
REQ = []

async def MAIN(message, args, level, perms, SERVER):
	if level == 1:
		await message.channel.send("Include a subcommand!")
		return
	
	if args[1].lower() == "setup":
		for _ in range(10):
			msg = await message.channel.send("\u200b")
	
	if args[1].lower() == "update":
		await message.channel.send("Updating list...")
		await SERVER["EVENTS"]["SIGNUPS"].update_list()
		await message.channel.send("Updated list!")
		return
	
	if args[1].lower() == "remove":
		msg = message.content

		if level == 2:
			await message.channel.send("Include the name of the TWOW you want to remove!")
			return
		
		db = Database()
		
		twow_name = " ".join(args[2:])

		twow_list = db.get_entries("signuptwows", conditions={"name": twow_name})

		if len(twow_list) == 0:
			await message.channel.send(f"There's no TWOW named **{twow_name}** in the signup list!")
			return
		
		twow_info = twow_list[0]
		dl_format = datetime.datetime.utcfromtimestamp(twow_info[4]).strftime("%d/%m/%Y %H:%M")

		db.remove_entry("signuptwows", conditions={"name": twow_name})

		await SERVER["EVENTS"]["SIGNUPS"].update_list()

		await message.channel.send(f"""**{twow_info[0]}** has been removed from the signup list!
		
		**TWOW Info**:
		""".replace("\t", "") + f"""name:[{twow_info[0]}] 
		host:[{twow_info[1]}] 
		link:[{twow_info[2]}] 
		desc:[{twow_info[3]}] 
		deadline:[{dl_format}] 
		{'is_verified' if bool(twow_info[5]) else ''}""".replace("\n", "").replace("\t", ""))

		return
		
	if args[1].lower() == "add":
		msg = message.content

		if "name:[" not in msg:
			await message.channel.send("Include the name of the TWOW you want to add!")
			return
		
		db = Database()
		
		starting_bound = msg[msg.find("name:[") + 6:]
		twow_name = starting_bound[:starting_bound.find("]")]

		entry = [twow_name, "", "", "", 0, 0, ""]
		
		if "host:[" in msg:
			starting_bound = msg[msg.find("host:[") + 6:]
			hosts = starting_bound[:starting_bound.find("]")]
			entry[1] = hosts
		
		if "link:[" in msg:
			starting_bound = msg[msg.find("link:[") + 6:]
			link = starting_bound[:starting_bound.find("]")]
			entry[2] = link
		
		if "desc:[":
			starting_bound = msg[msg.find("desc:[") + 6:]
			desc = starting_bound[:starting_bound.find("]")]
			entry[3] = desc
		
		if "deadline:[" in msg:
			starting_bound = msg[msg.find("deadline:[") + 10:]
			deadline = starting_bound[:starting_bound.find("]")]
			entry[6] = deadline
			deadline = datetime.datetime.strptime(deadline, "%d/%m/%Y %H:%M")
			deadline = deadline.replace(tzinfo=datetime.timezone.utc).timestamp()
			entry[4] = deadline
		
		verified = 0
		if "is_verified" in msg:
			verified = 1
		entry[5] = verified

		db.add_entry("signuptwows", entry[:6])
		await SERVER["EVENTS"]["SIGNUPS"].update_list()
		await message.channel.send(f"""**{entry[0]}** has been added to the list of TWOWs in signups!
		**Host:** {entry[1]}
		**Description:** {entry[3]}
		**Deadline:** {entry[6]}
		**Deadline Timestamp:** {entry[4]}
		**Link:** <{entry[2]}>""".replace("\t", ""))