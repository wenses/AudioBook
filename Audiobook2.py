from flet import *
from PdfLib import *
import pyttsx3 as tts

def main(page: Page):
	global title
	global fpath
	page.title="Blixen AudioBook"
	page.theme_mode='Dark'
	blue='#00edef'
	white='white'
	green='#00ff00'

	fplaying=Text('File Audio is playing...',color=green)
	pbar=ProgressBar(color=green)
	about='''
	This is an official open source software
	of Blixen Company, which is under Wenseslaus Bahati

	Any comments, suggestions, or critics contact blixentech7@gmail.com'''

	Ad=AlertDialog(
		title=Text("About Blixen AudioBook"),
		content=Text(about))
	

	#alert dialogs section of the code
	Ad0=AlertDialog(
		title=Text("Note"),
		content=Text("Play All files is set as default"))



	page.dialog=Ad
	Ad.open=True
	page.update()


	#function for the filepicker

	def fpr(e: FilePickerResultEvent):
		global fpath
		global total

		status.value=''
		lv.controls.pop()
		page.update()

		if len(e.files)==1:
			fname=e.files[0].name
			fpath=e.files[0].path

			total=ReadBook.get_pages(fpath)

		lv.controls.append(
			Text(f'File Loaded: {fname}',
				color=blue))
		page.update()

	#playing all pages
	def play_all(e):
		global speak
		tl=ReadBook.all_pages(fpath)
		lv.controls.append(fplaying)
		lv.controls.append(pbar)
		page.update()
		speak=tts.init()


		for c0 in tl:
			speak.say(c0)
			page.update()

		speak.runAndWait()

		lv.controls.remove(fplaying)
		lv.controls.remove(pbar)
		page.update()

	def stop_playing(e):
		speak.stop()
		lv.controls.remove(pbar)
		lv.controls.remove(fplaying)
		page.update()

	#functin for a single page
	def play_one(e):
		
		page.dialog=Ad1
		Ad1.open=True
		page.update()

	def play_one_action(e):
		global fpath
		global speak
		Ad1.open=False
		page.update()
		txt1=ReadBook.single_page(fpath,int(pageno.value))
		lv.controls.append(fplaying)
		lv.controls.append(pbar)
		page.update()
		speak=tts.init()
		speak.say(txt1)
		speak.runAndWait()
		lv.controls.remove(fplaying)
		lv.controls.remove(pbar)
		page.update()
		


	#alert dialog for single page
	pageno=TextField(hint_text='Enter Page number to play',
		on_submit=play_one_action)
	Ad1=AlertDialog(
		title=Text(f"Play One Page only,"),
		content=pageno,
		actions=[ElevatedButton('play',
			on_click=play_one_action)])

	#for section pages
	def play_section(e):
		page.dialog=Ad2
		Ad2.open=True
		page.update()

	def play_section_action(e):
		global fpath
		global speak
		Ad2.open=False
		page.update()

		tl2=ReadBook.section_pages(fpath,int(sp.value),int(ep.value	))
		lv.controls.append(fplaying)
		lv.controls.append(pbar)
		page.update()
		for _ in tl2:
			speak=tts.init()
			speak.say(_)
			speak.runAndWait()

		lv.controls.remove(fplaying)
		lv.controls.remove(pbar)
		page.update()
	sp=TextField(hint_text="Starting Page")
	ep=TextField(hint_text="Ending Page")

	Ad2=AlertDialog(
		title=Text("Play a range of custom pages"),
		content=Column(
			controls=[sp,ep]),
		actions=[ElevatedButton('play',
			on_click=play_section_action)])

	cb=ElevatedButton('choose a file'
				,bgcolor=blue,
				color=white,
				on_click=lambda _:fd.pick_files())

	options=PopupMenuButton(
		items=[
		PopupMenuItem(
			content=ElevatedButton('about'
				,bgcolor=blue
				,color=white))])
	#print(dir(options))

	page.appbar=AppBar(
		title=Text("Blixen AudioBook v1.0.0"),
		center_title=True,
		bgcolor=blue,
		actions=[options],
		color=white)

	lv=ListView(spacing=10)
	spage=Stack([lv])

	fd=FilePicker(on_result=fpr)
	page.overlay.append(fd)

	status=Text('No File Loaded...',color='#cecece')
	
	lv.controls.append(cb)
	lv.controls.append(status)
	page.update()



	play_options=PopupMenuButton(icon='menu',
		items=[
		PopupMenuItem(
			content=ElevatedButton('Play All Pages',
				on_click=play_all,
				bgcolor=blue,
				color=white)),
		PopupMenuItem(
			content=ElevatedButton('Play a single page',
				on_click=play_one,
				bgcolor=blue,
				color=white)),
		PopupMenuItem(
			content=ElevatedButton('Play a section of pages',
				on_click=play_section,
				bgcolor=blue,
				color=white))])
	stop_button=IconButton("stop",
			icon_color=white,
			on_click=stop_playing,
			bgcolor=blue)
#	print(dir(play_options))
	pp=Row(
		alignment='center',
		controls=[
		IconButton('play_circle',
			icon_color=white,
			on_click=play_all,
			bgcolor=blue,),
		play_options])

	page.add(spage,pp)




app(target=main)