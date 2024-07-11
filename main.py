import pickle
import random
import os
import time
import customtkinter as ctk


class ProjectHunter:
    SAVE_FILE = 'game_state.pkl'
    ACHIEVEMENTS = ['Novice Hunter', 'Skilled Hunter', 'Expert Hunter', 'You\'re a monster',
                    'You\'ve murdered so many, why?']
    INCREASE_MULTIPLIER = 2.5
    INITIAL_HUNT_SUCCESS_RATE = 0.05
    MAX_HUNT_SUCCESS_RATE = 1.00

    def __init__(self):
        self.init_game_state()
        self.app = ctk.CTk()
        self.setup_ui()
        self.load_state()

    def init_game_state(self):
        self.corpses = 0
        self.consumed = 0
        self.total_flesh_consumed = 0
        self.power = 1
        self.consumed_goal = 2
        self.hunt_success_rate = ProjectHunter.INITIAL_HUNT_SUCCESS_RATE
        self.clicks = 0
        self.total_corpses = 0
        self.achievements = {achievement: False for achievement in ProjectHunter.ACHIEVEMENTS}
        self.total_time_played = 0
        self.start_time = time.time()
        self.undeads = 0
        self.zombie = 0
        self.ghoul = 0
        self.zombie_cost = 1
        self.ghoul_cost = 2

    def setup_ui(self):
        self.app.title('Project Hunter v0.0.1')
        self.app.geometry('500x400')
        self.app.protocol('WM_DELETE_WINDOW', self.close_game)
        self.app.resizable(False, False)

        self.create_frames()
        self.create_main_frame_widgets()
        self.create_settings_frame_widgets()
        self.create_stats_frame_widgets()
        self.create_achievements_frame_widgets()
        self.create_credits_frame_widgets()
        self.create_shop_frame_widgets()

    def create_frames(self):
        self.main_frame = ctk.CTkFrame(self.app)
        self.settings_frame = ctk.CTkFrame(self.app)
        self.stats_frame = ctk.CTkFrame(self.app)
        self.achievements_frame = ctk.CTkFrame(self.app)
        self.credits_frame = ctk.CTkFrame(self.app)
        self.shop_frame = ctk.CTkFrame(self.app)

        for frame in (
                self.main_frame, self.settings_frame, self.stats_frame, self.achievements_frame, self.credits_frame,
                self.shop_frame):
            frame.grid(row=0, column=0, sticky='nsew')

    def create_main_frame_widgets(self):
        main_font = ctk.CTkFont(family='Comic Sans MS', size=18)
        edit_main_font = ctk.CTkFont(family='Comic Sans MS', size=14)

        self.num_consumed_label = ctk.CTkLabel(master=self.main_frame, text='', text_color='#800000', font=main_font)
        self.num_corpse_label = ctk.CTkLabel(master=self.main_frame, text='', text_color='#c20000', font=main_font)
        self.voices_in_head_label = ctk.CTkLabel(master=self.main_frame, text='Begin the rampage?',
                                                 text_color='#8B0000', font=main_font)
        self.power_blood_label = ctk.CTkLabel(master=self.main_frame, text='', text_color='#ab65f8', font=main_font)
        self.progress_bar = ctk.CTkProgressBar(master=self.main_frame, fg_color='#2F4F4F', progress_color='#800000',
                                               height=20, width=200)
        self.progress_bar.set(0)
        self.progress_bar_label = ctk.CTkLabel(master=self.main_frame, text='', font=edit_main_font)
        self.achievement_popup = ctk.CTkLabel(master=self.main_frame, text='', text_color='#FFD700', font=main_font)

        self.consume_btn = ctk.CTkButton(master=self.main_frame, text='RIP AND CONSUME UNTIL IT IS GONE',
                                         command=self.event_consume_btn,
                                         font=edit_main_font, corner_radius=32, fg_color='#2F4F4F',
                                         hover_color='#696969',
                                         border_color='#2e4045', border_width=2, text_color='#DCDCDC')
        self.hunt_btn = ctk.CTkButton(master=self.main_frame, text='Attempt to hunt?', command=self.event_hunt_btn,
                                      font=main_font, corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                      border_color='#2e4045', border_width=2, text_color='#DCDCDC')
        self.restart_btn = ctk.CTkButton(master=self.main_frame, text='Restart Nightmare', command=self.restart_save,
                                         font=edit_main_font, corner_radius=32, fg_color='#2F4F4F',
                                         hover_color='#696969',
                                         border_color='#2e4045', border_width=2, text_color='#DCDCDC')
        self.close_btn = ctk.CTkButton(master=self.main_frame, text='Close Nightmare', command=self.close_game,
                                       font=edit_main_font, corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                       border_color='#2e4045', border_width=2, text_color='#DCDCDC')
        self.settings_btn = ctk.CTkButton(master=self.main_frame, text='Settings',
                                          command=lambda: self.show_frame(self.settings_frame),
                                          font=edit_main_font, corner_radius=32, fg_color='#2F4F4F',
                                          hover_color='#696969',
                                          border_color='#2e4045', border_width=2, text_color='#DCDCDC')
        self.shop_btn = ctk.CTkButton(master=self.main_frame, text='Shop',
                                      command=lambda: self.show_frame(self.shop_frame),
                                      font=edit_main_font, corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                      border_color='#2e4045', border_width=2, text_color='#DCDCDC')

        self.hunt_btn.grid(row=0, column=0, padx=5, pady=5)
        self.consume_btn.grid(row=0, column=1, padx=5, pady=5)
        self.close_btn.grid(row=14, column=0, padx=3, pady=3)
        self.restart_btn.grid(row=15, column=0, padx=3, pady=3)
        self.settings_btn.grid(row=16, column=0, padx=5, pady=5)
        self.shop_btn.grid(row=17, column=0, padx=5, pady=5)
        self.num_corpse_label.grid(row=1, column=0, padx=5, pady=5)
        self.num_consumed_label.grid(row=1, column=1, padx=5, pady=5)
        self.voices_in_head_label.grid(row=4, column=0, columnspan=2, pady=5)
        self.power_blood_label.grid(row=8, column=0, columnspan=3, pady=5)
        self.progress_bar.grid(row=13, column=0, padx=5, pady=5, columnspan=3)
        self.progress_bar_label.grid(row=4, column=2, padx=5, pady=5)
        self.achievement_popup.grid(row=7, column=0, columnspan=3, pady=10)

    def create_settings_frame_widgets(self):
        edit_main_font = ctk.CTkFont(family='Comic Sans MS', size=14)

        stats_btn = ctk.CTkButton(master=self.settings_frame, text='Stats',
                                  command=lambda: self.show_frame(self.stats_frame),
                                  font=edit_main_font, corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                  border_color='#2e4045', border_width=2, text_color='#DCDCDC')
        achievements_btn = ctk.CTkButton(master=self.settings_frame, text='Achievements',
                                         command=lambda: self.show_frame(self.achievements_frame),
                                         font=edit_main_font, corner_radius=32, fg_color='#2F4F4F',
                                         hover_color='#696969',
                                         border_color='#2e4045', border_width=2, text_color='#DCDCDC')
        credits_btn = ctk.CTkButton(master=self.settings_frame, text='Credits',
                                    command=lambda: self.show_frame(self.credits_frame),
                                    font=edit_main_font, corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                    border_color='#2e4045', border_width=2, text_color='#DCDCDC')
        back_btn = ctk.CTkButton(master=self.settings_frame, text='Back',
                                 command=lambda: self.show_frame(self.main_frame),
                                 font=edit_main_font, corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                 border_color='#2e4045', border_width=2, text_color='#DCDCDC')

        stats_btn.pack(pady=10)
        achievements_btn.pack(pady=10)
        credits_btn.pack(pady=10)
        back_btn.pack(pady=10)

    def create_stats_frame_widgets(self):
        edit_main_font = ctk.CTkFont(family='Comic Sans MS', size=14)

        self.stats_label = ctk.CTkLabel(master=self.stats_frame, text='', font=edit_main_font)
        back1_btn = ctk.CTkButton(master=self.stats_frame, text='Back',
                                  command=lambda: self.show_frame(self.settings_frame),
                                  font=edit_main_font, corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                  border_color='#2e4045', border_width=2, text_color='#DCDCDC')

        self.stats_label.pack(pady=20)
        back1_btn.pack(pady=10)

    def create_achievements_frame_widgets(self):
        edit_main_font = ctk.CTkFont(family='Comic Sans MS', size=14)

        self.achievements_label = ctk.CTkLabel(master=self.achievements_frame, text='', font=edit_main_font)
        back2_btn = ctk.CTkButton(master=self.achievements_frame, text='Back',
                                  command=lambda: self.show_frame(self.settings_frame),
                                  font=edit_main_font, corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                  border_color='#2e4045', border_width=2, text_color='#DCDCDC')

        self.achievements_label.pack(pady=20)
        back2_btn.pack(pady=10)

    def create_credits_frame_widgets(self):
        edit_main_font = ctk.CTkFont(family='Comic Sans MS', size=14)

        self.credits_label = ctk.CTkLabel(master=self.credits_frame, text='', font=edit_main_font)
        back3_btn = ctk.CTkButton(master=self.credits_frame, text='Back',
                                  command=lambda: self.show_frame(self.settings_frame),
                                  font=edit_main_font, corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                  border_color='#2e4045', border_width=2, text_color='#DCDCDC')

        self.credits_label.pack(pady=20)
        back3_btn.pack(pady=10)

    def create_shop_frame_widgets(self):
        main_font = ctk.CTkFont(family='Comic Sans MS', size=18)
        edit_main_font = ctk.CTkFont(family='Comic Sans MS', size=14)

        self.shop_label = ctk.CTkLabel(master=self.shop_frame, text='Shop', font=main_font)
        self.undead_label = ctk.CTkLabel(master=self.shop_frame, text='', font=edit_main_font)
        self.buy_zombie_btn = ctk.CTkButton(master=self.shop_frame, command=self.buy_zombie, font=edit_main_font,
                                            corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                            border_color='#2e4045', border_width=2, text_color='#DCDCDC')
        self.buy_ghoul_btn = ctk.CTkButton(master=self.shop_frame, command=self.buy_ghoul, font=edit_main_font,
                                           corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                           border_color='#2e4045', border_width=2, text_color='#DCDCDC')
        shop_back_btn = ctk.CTkButton(master=self.shop_frame, text='Back',
                                      command=lambda: self.show_frame(self.main_frame),
                                      font=edit_main_font, corner_radius=32, fg_color='#2F4F4F', hover_color='#696969',
                                      border_color='#2e4045', border_width=2, text_color='#DCDCDC')

        self.shop_label.pack(pady=20)
        self.undead_label.pack(pady=10)
        self.buy_zombie_btn.pack(pady=10)
        self.buy_ghoul_btn.pack(pady=10)
        shop_back_btn.pack(pady=10)

    def load_state(self):
        if os.path.exists(ProjectHunter.SAVE_FILE):
            with open(ProjectHunter.SAVE_FILE, 'rb') as f:
                state = pickle.load(f)
                self.restore_state(state)
        self.update_ui()

    def restore_state(self, state):
        if len(state) == 15:  # handle old state format
            (self.corpses, self.consumed, self.total_flesh_consumed, self.power, self.consumed_goal, self.zombie_cost,
             self.hunt_success_rate, self.clicks, self.total_corpses, self.achievements, self.zombie, self.ghoul,
             self.total_time_played, self.undeads, self.ghoul_cost) = state
            self.hunt_success_rate = ProjectHunter.INITIAL_HUNT_SUCCESS_RATE
        elif len(state) == 15:  # handle new state format
            (self.corpses, self.consumed, self.total_flesh_consumed, self.power, self.consumed_goal, self.zombie_cost,
             self.hunt_success_rate, self.clicks, self.total_corpses, self.achievements, self.zombie, self.ghoul,
             self.total_time_played, self.undeads, self.ghoul_cost) = state

    def save_state(self):
        self.total_time_played += time.time() - self.start_time
        state = (self.corpses, self.consumed, self.total_flesh_consumed, self.power, self.consumed_goal,
                 self.zombie_cost, self.hunt_success_rate, self.clicks, self.total_corpses, self.achievements,
                 self.zombie, self.ghoul, self.total_time_played, self.undeads, self.ghoul_cost)
        with open(ProjectHunter.SAVE_FILE, 'wb') as f:
            pickle.dump(state, f)
        self.start_time = time.time()

    def update_ui(self):
        self.num_corpse_label.configure(text=f'{self.corpses} corpse(s)')
        self.num_consumed_label.configure(text=f'{self.consumed} flesh consumed')
        self.power_blood_label.configure(text=f'{self.power} power')
        self.progress_bar_label.configure(text=f'{self.consumed}/{self.consumed_goal} flesh consumed')
        self.progress_bar.set(self.consumed / self.consumed_goal)

        elapsed_time = self.total_time_played + (time.time() - self.start_time)
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        self.stats_label.configure(
            text=f'clicks (all time): {self.clicks}\ncorpses (all time): {self.total_corpses}\n'
                 f'flesh consumed (all time): {self.total_flesh_consumed}\nsuccessful hunt chance: '
                 f'{self.hunt_success_rate * 100:.2f}%\ntime played (all time): {elapsed_time_str}')

        achievement_text = 'Achievements:\n'
        for achievement, unlocked in self.achievements.items():
            if achievement in ['You\'re a monster', 'You\'ve murdered so many, why?'] and not unlocked:
                achievement_text += 'Achievement Locked: [Redacted]\n'
            else:
                status = 'Unlocked' if unlocked else 'Locked'
                achievement_text += f'Achievement {status}: {achievement}\n'
        self.achievements_label.configure(text=achievement_text.strip())
        self.credits_label.configure(text=f'made by apoptoses.\n coded using python')
        self.undead_label.configure(text=f'Undeads: {self.undeads}')
        self.buy_zombie_btn.configure(text=f'Zombie Cost: {self.zombie_cost}')
        self.buy_ghoul_btn.configure(text=f'Ghoul Cost: {self.ghoul_cost}')

    def event_hunt_btn(self):
        if random.random() < self.hunt_success_rate:
            self.corpses += 1
            self.voices_in_head_label.configure(text='Successful hunt', text_color='#8B0000')
            self.total_corpses += 1
        else:
            self.voices_in_head_label.configure(text='Hunt failed', text_color='#A52A2A')
        self.clicks += 1
        self.check_achievements()
        self.update_ui()

    def event_consume_btn(self):
        if self.corpses < 1:
            self.voices_in_head_label.configure(text='where...?', text_color='#A52A2A')
        else:
            self.consumed += 1
            self.total_flesh_consumed += 1
            self.corpses -= 1
            self.voices_in_head_label.configure(text='whose flesh was it...', text_color='#8B0000')
            if self.consumed >= self.consumed_goal:
                self.power += 1
                self.consumed = 0
                self.consumed_goal *= ProjectHunter.INCREASE_MULTIPLIER
                self.hunt_success_rate = min(self.hunt_success_rate + 0.01, ProjectHunter.MAX_HUNT_SUCCESS_RATE)
        self.update_ui()

    def buy_zombie(self):
        if self.corpses >= self.zombie_cost:
            self.corpses -= self.zombie_cost
            self.zombie_cost *= ProjectHunter.INCREASE_MULTIPLIER
            self.zombie += 1
            self.undeads += 1
        self.update_ui()

    def increment_corpses_by_zombie(self):
        self.corpses += self.zombie
        self.total_corpses += self.zombie
        self.app.after(10000, self.increment_corpses_by_zombie)
        self.update_ui()

    def buy_ghoul(self):
        if self.corpses >= self.ghoul_cost:
            self.corpses -= self.ghoul_cost
            self.ghoul_cost *= ProjectHunter.INCREASE_MULTIPLIER
            self.ghoul += 1
            self.undeads += 1
        self.update_ui()

    def increment_corpses_by_ghoul(self):
        self.corpses += self.ghoul
        self.total_corpses += self.ghoul
        self.update_ui()
        self.app.after(3333, self.increment_corpses_by_ghoul)
        self.increment_corpses_by_ghoul()

    def check_achievements(self):
        achievements_unlocked = []
        if self.clicks >= 10000 and not self.achievements['You\'ve murdered so many, why?']:
            self.achievements['You\'ve murdered so many, why?'] = True
            achievements_unlocked.append('You\'ve murdered so many, why?')
        if self.clicks >= 5000 and not self.achievements['You\'re a monster']:
            self.achievements['You\'re a monster'] = True
            achievements_unlocked.append('You\'re a monster')
        if self.clicks >= 2000 and not self.achievements['Expert Hunter']:
            self.achievements['Expert Hunter'] = True
            achievements_unlocked.append('Expert Hunter')
        if self.clicks >= 500 and not self.achievements['Skilled Hunter']:
            self.achievements['Skilled Hunter'] = True
            achievements_unlocked.append('Skilled Hunter')
        if self.clicks >= 100 and not self.achievements['Novice Hunter']:
            self.achievements['Novice Hunter'] = True
            achievements_unlocked.append('Novice Hunter')

        for achievement in achievements_unlocked:
            self.display_achievement_popup(achievement)

    def display_achievement_popup(self, achievement):
        self.achievement_popup.configure(text=f'Achievement Unlocked: {achievement}')
        self.achievement_popup.grid()
        self.app.after(3000, self.clear_achievement_popup)

    def clear_achievement_popup(self):
        self.achievement_popup.grid_remove()

    def close_game(self):
        self.update_ui()
        self.save_state()
        self.app.destroy()

    def restart_save(self):
        self.voices_in_head_label.configure(text='Nightmare rebegins')
        self.reset_game_state()
        self.save_state()
        self.update_ui()

    def reset_game_state(self):
        self.init_game_state()

    def show_frame(self, frame):
        frame.tkraise()

    def run(self):
        self.show_frame(self.main_frame)
        self.app.mainloop()


if __name__ == "__main__":
    game = ProjectHunter()
    game.run()
