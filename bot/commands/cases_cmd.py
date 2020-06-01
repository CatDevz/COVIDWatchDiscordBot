import discord, datetime, time, calendar
from bot.commands.command import Command
from bot.daemons.update_data import UpdateData


class CasesCMD(Command):
    async def run(self, message, raw_args):
        scope = "global"

        args = []
        for rarg in raw_args.split('-'):
            arg = rarg.split(' ')
            for i in arg:
                if i == '':
                    arg.remove('')
            if len(arg) > 0:
                args.append(arg)

        for arg in args:
            if len(arg) < 1:
                continue
            if arg[0] == "country" or arg[0] == "c":
                if len(arg) > 1:
                    scope = ""
                    for scopeArg in arg[1:]:
                        scope = scope + str(scopeArg)
                        if scopeArg != arg[len(arg)-1]:
                            scope = scope + " "

                    # Adding special cases to countries that should have them
                    if scope.lower() == "usa" or scope.lower() == "united states":
                        scope = "US"
                else:
                    await message.channel.send("**`You must enter the name of a country you would like to scope into.`**")

        if self.covidData.req: #Im afraid the country you selected could not be found, maybe there was a spelling mistake?
            if scope.lower() == "global":
                res_g = self.covidData.results['Global']
                title = "COVID19 Cases Globally"
                # url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/International_Flag_of_Planet_Earth.svg/800px-International_Flag_of_Planet_Earth.svg.png"
            else:
                for country in self.covidData.results['Countries']:
                    if country['Country'].lower() == scope.lower() or country['CountryCode'].lower() == scope.lower() or country['Slug'] == scope.lower():
                        res_g = country
                        title = "COVID19 Cases | :flag_{}:".format(country['CountryCode'].lower())
                        # url = "https://www.countryflags.io/" + country['CountryCode'].lower() + "/flat/64.png"
                        break

            try:
                embed = discord.Embed(
                    title=title,
                    description="Please **[vote](https://top.gg/bot/708929935443492995)** for my bot on **top.gg** | All data from **[covid19api](https://covid19api.com/)** \nStatistics last updated **{}**".format(str(self.covidData.results['Countries'][0]['Date'])),
                    colour=discord.Colour(0x9c0519),
                    timestamp=datetime.datetime.utcfromtimestamp(calendar.timegm(time.gmtime()))
                )
                embed.set_footer(text="Covid Watch - Coronavirus Statistics",
                                 icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/SARS-CoV-2_without_background.png/220px-SARS-CoV-2_without_background.png")

                death_rate = str(int(str(res_g['TotalDeaths']).replace(',', '')) / int(
                    str(res_g['TotalConfirmed']).replace(',', '')) * 100)
                death_rate = death_rate[:6] + "%"
                active_cases = res_g['TotalConfirmed'] - res_g['TotalDeaths'] - res_g['TotalRecovered']

                embed.add_field(name=":biohazard: Confirmed Cases",
                                value='**{:,}** (+{:,})'.format(res_g['TotalConfirmed'], res_g['NewConfirmed']))
                embed.add_field(name=":heart: Recovered",
                                value='**{:,}** (+{:,})'.format(res_g['TotalRecovered'], res_g['NewRecovered']))
                embed.add_field(name=":skull_crossbones: Deaths",
                                value='**{:,}** (+{:,})'.format(res_g['TotalDeaths'], res_g['NewDeaths']))
                embed.add_field(name=":nauseated_face: Active Cases",
                                value='**{:,}**'.format(active_cases))
                embed.add_field(name=":grey_exclamation: Death Rate",
                                value='**{}**'.format(death_rate))
                embed.add_field(name=":grey_exclamation: Cases Per Million",
                                value='**{}**'.format('0'))
                await message.channel.send(embed=embed)
            except UnboundLocalError:
                await message.channel.send("Country {} was not found.".format(scope))
        else:
            await message.channel.send("**`Covid api returned status code {}. Please wait a minute then rerun this command as these issues usually fix themselves.`**".format(self.covidData.unstable_req.status_code))

    def init(self):
        self.covidData = UpdateData()