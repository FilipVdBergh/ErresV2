import libLCDUI.libLCDUI as libLCDUI
import pylms.server
from erres_variables import *
import time

class Interface(object):
    def __init__(self, display, server, player):
        self.ui = libLCDUI.ui(display, width=20, height=4)
        self.server_address = server
        self.player_name = player
        self.server = None
        self.player = None
        self.all_players = []
        self.all_favorites = []
        self.power = True
        self.mode = 0
        self.modes = {0: ["Now playing", "~[RIGHT]"],
                      1: ["Skip", "~[NOTE]"],
                      2: ["Favorites", "~[HEART]"],
                      3: ["Info", "~[FOLDER]"],
                      4: ["Sync", "~[SYNC]"],
                      -1: ["Off", " "]}
        self.alert_pause = 2


        self.txtDateTime = libLCDUI.text(20,2)
        self.txtDateTime.format(libLCDUI.center)
        self.icoMode = libLCDUI.text(1,1)
        self.barVolume = libLCDUI.vertical_progress_bar(1,3,0,100)
        self.txtVolumeOverlay = libLCDUI.text(20,4)
        self.txtVolumeOverlay.format(libLCDUI.center)
        self.txtVolumeOverlay.write(["","Volume","",""])
        self.barVolumeLarge = libLCDUI.horizontal_progress_bar(16,1,0,100)
        self.txtVolumeValue = libLCDUI.text(2,1)
        self.txtNowPlaying = libLCDUI.text(18,3)
        self.lstFavorites = libLCDUI.list(18,4)
        self.lstFavorites.set_indicator("~[RIGHT_SMALL]", " ")
        self.lstTechnicalInfo = libLCDUI.list(18, 4)
        self.lstTechnicalInfo.set_indicator("~[RIGHT_SMALL]", " ")
        self.lstPlayers = libLCDUI.list(18,4)
        self.lstPlayers.set_indicator("~[RIGHT_SMALL]", " ")
        self.txtTrackCounter = libLCDUI.text(18, 1)
        self.txtTrackCounter.format(libLCDUI.right)
        self.txtTimeCounter = libLCDUI.text(18, 1)
        self.txtTimeCounter.format(libLCDUI.right)
        self.txtAlert = libLCDUI.text(18, 4)

        self.txtDateTime.hide()
        self.txtAlert.hide()
        self.barVolumeLarge.hide()
        self.txtVolumeOverlay.hide()
        self.txtVolumeValue.hide()

        self.ui.add_widget(self.txtDateTime,1,0)
        self.ui.add_widget(self.icoMode,0,0)
        self.ui.add_widget(self.barVolume,1,0)
        self.ui.add_widget(self.txtNowPlaying,0,2)
        self.ui.add_widget(self.lstFavorites,0,2)
        self.ui.add_widget(self.lstTechnicalInfo, 0, 2)
        self.ui.add_widget(self.lstPlayers,0,2)
        self.ui.add_widget(self.txtTrackCounter,3,2)
        self.ui.add_widget(self.txtTimeCounter,3,2)
        self.ui.add_widget(self.txtVolumeOverlay,0,0)
        self.ui.add_widget(self.txtVolumeValue, 2, 0)
        self.ui.add_widget(self.barVolumeLarge, 2, 3)
        self.ui.add_widget(self.txtAlert,0,2)

        self.layouts = {0: [self.icoMode, self.barVolume, self.txtNowPlaying, self.txtTimeCounter],
                        1: [self.icoMode, self.barVolume, self.txtNowPlaying, self.txtTrackCounter],
                        2: [self.icoMode, self.barVolume, self.lstFavorites],
                        3: [self.icoMode, self.barVolume, self.lstTechnicalInfo],
                        4: [self.icoMode, self.barVolume, self.lstPlayers],
                        -1: [self.txtDateTime]}
        self.colors  = {0: [LCD_red, LCD_green, LCD_blue],
                        1: [LCD_red, LCD_green, LCD_blue],
                        2: [LCD_red, LCD_green, LCD_blue],
                        3: [LCD_red, LCD_green, LCD_blue],
                        4: [LCD_red, LCD_green, LCD_blue],
                        -1: [LCD_off_red, LCD_off_green, LCD_off_blue]}
        self.change_mode_to(0)
        self.connect()

    def connect(self):
        self.txtAlert.write(["Connecting to", self.server_address])
        self.txtAlert.show()
        success = False
        while not(success):
            self.ui.redraw()
            try:
                self.server = pylms.server.Server(self.server_address)
                self.server.connect()
                success = True
            except:
                time.sleep(pauseBetweenRetries)
        self.txtAlert.write(["Registering player", self.player_name])
        success = False
        while not(success):
            self.ui.redraw()
            try:
                self.player = self.server.get_player(self.player_name)
                success = True
            except:
                time.sleep(pauseBetweenRetries)

        # Populate several lists
        self.txtAlert.write("Getting list of players")
        self.all_players = self.server.get_players()
        self.all_favorites = self.server.get_favorites()
        print self.all_favorites
        self.txtAlert.write("Connected")
        self.txtAlert.start_countdown(self.alert_pause)
        self.redraw()

    def is_connected(self):
        try:
            self.player.get_ip_address()
            return True
        except:
            return False

    def change_mode_to(self, mode):
        if mode in self.modes:
            self.mode = mode
            self.change_layout()


    def change_mode_by(self, step):
        self.mode += step
        if self.mode > max(self.modes):
            self.mode = 0
        if self.mode < 0:
            self.mode = max(self.modes)
        self.change_layout()

    def get_mode(self, by_name=False):
        if by_name:
            return self.modes[self.mode][0]
        else:
            return self.mode

    def switch_power(self, state=None):
        if state is None:
            self.player.set_power_state(not self.player.get_power_state())
        else:
            self.player.set_power_state = state
        self.power = self.player.get_power_state()
        self.change_layout()

    def change_volume(self, amount):
        if amount > 0:
            self.player.volume_up(amount)
        else:
            self.player.volume_down(-amount)
        self.barVolumeLarge.start_countdown(1)
        self.txtVolumeOverlay.start_countdown(1)
        self.txtVolumeValue.start_countdown(1)

    def show_info(self, i):
        if i == 0:
            self.txtAlert.write(self.player.get_track_artist())
        elif i == 1:
            self.txtAlert.write(self.player.get_track_title())
        elif i == 2:
            self.txtAlert.write(self.player.get_track_album())
        elif i == 3:
            self.txtAlert.write(self.player.get_name())
        elif i == 4:
            self.txtAlert.write(self.player.get_ip_address())
        elif i == 5:
            self.txtAlert.write(self.player.get_mode())
        elif i == 6:
            self.txtAlert.write(self.server_address)
        self.txtAlert.start_countdown(3)

    def change_layout(self):
        self.ui.display.set_color(self.colors[self.mode][0], self.colors[self.mode][1], self.colors[self.mode][2])

        # Change the icon to the icon for the current mode:
        self.icoMode.write([self.modes[self.mode][1]])

        # Enable widgets in the current layout and disable the rest:
        for widget in self.ui.list_widgets():
            if widget in self.layouts[self.mode]:
                widget.show()
            else:
                widget.hide()

        if self.mode == 2:
            self.lstFavorites.clear()
            for f in self.all_favorites:
                self.lstFavorites.add_item(f['name'])

        if self.mode == 3:
            self.lstTechnicalInfo.clear()
            self.lstTechnicalInfo.add_item("Artist: "+self.player.get_track_artist())
            self.lstTechnicalInfo.add_item("Title : "+self.player.get_track_title())
            self.lstTechnicalInfo.add_item("Album : "+self.player.get_track_album())
            self.lstTechnicalInfo.add_item("Player: "+self.player.get_name())
            self.lstTechnicalInfo.add_item("IP    : "+self.player.get_ip_address())
            self.lstTechnicalInfo.add_item("Mode  : "+self.player.get_mode())
            self.lstTechnicalInfo.add_item("Server: "+self.server_address)

        if self.mode == 4:
            self.lstPlayers.clear()
            for p in self.all_players:
                self.lstPlayers.add_item(p.get_name())

    def user_input(self, button, value):
        # This function  handles all user input (button presses and turns).
        if button == 1:
            if self.is_connected():
                self.player.set_power_state(not self.player.get_power_state())
                if self.player.get_power_state():
                    self.change_mode_to(0)
                    self.player.play()
                else:
                    self.change_mode_to(-1)
        elif button == 2:
            if self.is_connected():
                if self.mode == 0:
                    self.player.toggle()
                if self.mode == 1:
                    self.player.toggle()
                if self.mode == 2:
                    self.player.playlist_play(self.all_favorites[self.lstFavorites.get_selected()]['url'])
                    self.txtAlert.write("Selected %s" % self.all_favorites[self.lstFavorites.get_selected()]['name'])
                    self.change_mode_to(0)
                    self.txtAlert.start_countdown(self.alert_pause)
                if self.mode == 3:
                    self.show_info(self.lstTechnicalInfo.get_selected())
                if self.mode == 4:
                    if self.player.is_synced():
                        self.player.unsync()
                        self.txtAlert.write("Unsynced player")
                    else:
                        self.all_players[self.lstPlayers.get_selected()].sync_to(self.player.get_ref())
                        self.txtAlert.write("Synced to %s" % self.all_players[self.lstPlayers.get_selected()].get_name())
                    self.change_mode_to(0)
                    self.txtAlert.start_countdown(self.alert_pause)
        elif button == 3:
                self.change_mode_to(0)
        elif button == 4:
            if self.is_connected():
                self.change_volume(value)
        elif button == 5:
            if self.is_connected():
                if self.mode == 0:
                    if value > 0:
                        self.player.forward(30)
                    else:
                        self.player.rewind(30)
                elif self.mode == 1:
                    if value > 0:
                        self.player.next()
                    else:
                        self.player.prev()
                elif self.mode == 2:
                    if value > 0:
                        self.lstFavorites.move_down()
                    else:
                        self.lstFavorites.move_up()
                elif self.mode == 3:
                    if value > 0:
                        self.lstTechnicalInfo.move_down()
                    else:
                        self.lstTechnicalInfo.move_up()
                elif self.mode == 4:
                    if value > 0:
                        self.lstPlayers.move_down()
                    else:
                        self.lstPlayers.move_up()
        elif button == 6:
            if self.is_connected():
                if value > 0:
                    self.change_mode_by(-1)
                else:
                    self.change_mode_by(+1)

    def redraw(self):
        if not self.player.get_power_state():
            self.change_mode_to(-1)
        else:
            if self.get_mode() == -1:
                self.change_mode_to(0)
                self.player.play()
        if self.is_connected():
            self.txtDateTime.write("- %s -" % self.player_name)
            self.txtNowPlaying.write("%s by %s" % (self.player.get_track_title(), self.player.get_track_artist()))
            self.barVolumeLarge.write(self.player.get_volume())
            self.barVolume.write(self.player.get_volume())
            self.txtVolumeValue.write(self.player.get_volume())
            self.txtTrackCounter.write("~[LEFT]%s/%s~[RIGHT]" % (self.player.playlist_current_track_index(), self.player.playlist_track_count()))
            self.txtTimeCounter.write("~[LEFT]%s/%s~[RIGHT]" % (self.time_format(self.player.get_time_elapsed()), self.time_format(self.player.get_track_duration())))
        self.ui.redraw()

    def time_format(self, duration):
        if duration > 3600:
            return time.strftime("%-H:", time.gmtime(duration))
        else:
            return time.strftime("%M:%S", time.gmtime(duration))