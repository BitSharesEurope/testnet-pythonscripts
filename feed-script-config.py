#!/usr/bin/env python3

################################################################################
##
##                D E F A U L T    C O N F I G U R A T I O N
##
##   This configuration represents a working example. Prices published are very
##   close to what they "should be". However, every witness has to judge on his
##   own as to whether these settings fit his needs.
##
################################################################################

import subprocess
import os
import feedsources
core_symbol = "BTS"
feedsources.core_symbol = core_symbol

################################################################################
## RPC-client connection information (required)
################################################################################
host   = "localhost"     # machine that runs a cli-wallet with -H parameter
port   = 8092            # RPC port, e.g.`-H 127.0.0.1:8092`
user   = ""              # API user (optional)
passwd = ""              # API user passphrase (optional)
unlock = ""              # password to unlock the wallet if the cli-wallet is locked

################################################################################
## Script runtime parameters
################################################################################
ask_confirmation             = False  # if true, a manual confirmation is required

################################################################################
## Witness Feed Publish Parameters
################################################################################
producer_name                = "fakeusd-feed-producer"

################################################################################
## Publishing Criteria
################################################################################
#
# Publish price if any of these are valid:
#
#  1.) price feed is older than maxAgeFeedInSeconds
#  2.) price has moved from my last published price by more than change_min
#
# Do NOT publish if
#
#  * Price has moved more than 'change_max'
#     AND
#  * Manual confirmation is 'false'
#
# A feed becomes invalid if it is older than 24h. Hence, it should be force
# published once a day (e.g. every 12h) Note that the script should be run more
# frequently and publishes only those prices that fit the publishing criteria
maxAgeFeedInSeconds          = 12 * 60 * 60  # max age of 12h
change_min                   = 0.5       # Percentage of price change to force an update
change_max                   = 5.0       # Percentage of price change to cause a warning

################################################################################
## Asset specific Settings
################################################################################
_all_assets = ["SILVER", "GOLD", "CNY", "EUR", "USD"]
_bases = ["CNY", "USD", "BTC", "EUR"]

asset_config = {
                   "default" : { ## DEFAULT BEHAVIOR
                       #
                       # how to derive a single price from several sources
                       # Choose from: "median", "mean", or "weighted" (by volume)
                       "metric" : "weighted",
                       #
                       # Select sources for this particular asset. Each source
                       # has its own fetch() method and collects several markets
                       # any market of an exchanges is considered but only the
                       # current asset's price is derived
                       # 
                       # Choose from: - "*": all,
                       #              - loaded exchanges (see below)
                       "sources" : [
                                    ## Required Exchanges for FIAT
                                    "btcavg",    # To get from BTC into USD/CNY/EUR
                                    #"yahoo",     # To get from USD/CNY/EUR into other FIAT currencies
                                    ## BTC/BTS exchanges (include BTC/* if available)
                                    "poloniex",
                                    #"ccedk",
                                    #"bittrex",
                                    #"btc38",
                                    #"yunbi",
                                    ## BTC/* exchanges
                                    #"okcoin",   # no trading-fees
                                    #"btcchina", # no trading-fees
                                    #"huobi",    # no trading-fees
                                    ],
                       # Core exchange factor for paying transaction fees in
                       # non-BTS assets. This is a factor: 0.95 = 95%
                       "core_exchange_factor"          : 0.95,
                       # Call when collateral only pays off 175% the debt. 
                       # This is denoted as: 1750 = 175% = 1.75
                       "maintenance_collateral_ratio"  : 1750,
                       # Stop calling when collateral only pays off 110% of the debt
                       # This is denoted as: 1100 = 110% = 1.10
                       "maximum_short_squeeze_ratio"   : 1001,
                   },
               }

## Other assets that are derived or something else.
## Currently available:
##
##    "sameas" : x     ## uses the same asset price as a MPA above
##
##
## Note: 
##  The usual asset specific parameters have to be set in "asset_config",
##  otherwise they will be ignored!
secondary_mpas = {
                    "PEG.FAKEUSD" : {
                                "sameas" : "USD"
                             },
                 }

################################################################################
## Exchanges and settings
## 
## scaleVolumeBy: a multiplicative factor for the volume
## allowFailure:  bool variable that will (if not set or set to False) exit the
##                script on error
################################################################################
feedSources = {}
#feedSources["yahoo"]    = feedsources.Yahoo()
feedSources["btcavg"]   = feedsources.BitcoinAverage()
#
feedSources["poloniex"] = feedsources.Poloniex(allowFailure=True)
#feedSources["ccedk"]    = feedsources.Ccedk(allowFailure=True)
#feedSources["bittrex"]  = feedsources.Bittrex(allowFailure=True)
#feedSources["yunbi"]    = feedsources.Yunbi(allowFailure=True)
#feedSources["btc38"]    = feedsources.Btc38(allowFailure=True)
#
#feedSources["btcchina"] = feedsources.BtcChina(allowFailure=True)
#feedSources["okcoin"]   = feedsources.Okcoin(allowFailure=True)
#feedSources["huobi"]    = feedsources.Huobi(allowFailure=True)
#
#feedSources["btcid"]    = feedsources.BitcoinIndonesia(allowFailure=True)
#feedSources["bter"]     = feedsources.Bter(allowFailure=True)

################################################################################
# Blame mode allows to verify old published prices
# All data requires is stored in the blame/ directoy. Filename is the head block
# number at the time of script execution.
# To recover a price (will not publish) simply set blame to the block number of
# an existing(!) file.
#
# Default: "latest"  # Will fetch prices from exchanges and publish it
################################################################################
blame = "latest"
#blame = "1428190"

################################################################################
# Git revision for storage in blame files
# (do not touch this line)
################################################################################
try :
    configPath = os.path.dirname(__file__)
    gittag = subprocess.check_output(["git", "-C", configPath, "rev-parse", "HEAD"]).decode("ascii").strip("\n")
except :
    pass

# coding=utf8 sw=4 expandtab ft=python
