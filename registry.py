import os
import subprocess
import requests as req
from pandas import DataFrame
from getpass import getpass
import re
import time

# TODO: setup GUI to get input and display table of results; 
# See kivy for GUI: https://kivy.org/doc/stable/gettingstarted/installation.html
# TODO: install password store and configure client environment to use password store
# TODO: install docker credentials helper in password store


class registry(object):
    #####################################################################
    def __init__(self, url=None,username=None,passenv=None,passwd=str) -> None:
        self.url = url
        self.username = username
        self.passenv = passenv
        self.passwd = passwd
        # print('password: {}'.format(passwd))
        # super().__init__()

    #####################################################################    
    def get_registry(self,url,username,passenv) -> DataFrame:
        """
        Gets the contents of your private container registry and organizes them into a table.

        This function uses "pass" as its password store. It takes your password store path to user password and accesses your password store securely.
        
        :param url: The registry URL
        :param username: The user account
        :param passenv: The user password environmental variable
        """
        tbl = []
        try:
            url = url if re.search('/v2', url) else '{}/v2'.format(url)
            # rauth = passenv if os.environ[passenv] is None else os.environ[passenv]
            rauth = os.error('Env returned null...') if re.search(passenv,os.environ[passenv]) else os.environ[passenv]
            # print('Docker Credential Token: {}\n'.format(rauth))
            # we are using a password store to access passwords on needed
            passwd = subprocess.check_output(["pass", rauth])
            passwd = passwd.decode("utf-8")
            # username = input("Enter Username: ")
            # passw = getpass("Enter Password: ")
            # print(passwd)
            uauth = (username,passwd)
            catelog = '{}/_catalog/'.format(url)
            # print(catelog)
            catelog = req.get(catelog, auth=uauth,timeout=(5, 10))   
            # print(catelog.json())
            for a in catelog.json()['repositories']:
                # print(a)
                item_details = '{0}/{1}/tags/list/'.format(url,a)
                rsp = req.get(item_details, auth=uauth)
                json_rsp = rsp.json()
                # print(json_rsp)
                tbl.append(json_rsp)
                # print('[{} => {}]'.format(json_rsp['name'], json_rsp['tags']))
            # print(tbl)
            df = DataFrame(data=tbl)
            print('\n{}\n'.format(df))
            # return df
        except req.exceptions.TooManyRedirects as err:
            print('{}'.format(err))
        except req.exceptions.ConnectionError as err:
            print('{}'.format(err))
        except req.exceptions.URLRequired as err:
            print('{}'.format(err))
        except req.exceptions.StreamConsumedError as err:
            print('{}'.format(err))
        except req.exceptions.ConnectTimeout as err:
            print('{}'.format(err))
        except req.exceptions.HTTPError as err:
            print('{}'.format(err))
        except req.exceptions.RequestException as err:
            print('{}'.format(err))
        except req.exceptions.Timeout as err:
            print('{}'.format(err))
        except OSError as err:
            print('Their was an error in your environment variable; parameter 2. \n{}'.format(err))
        except KeyError as err:
            print(f'The environment variable {err} does not match any found in our system.')
    #####################################################################
#########################################################################
if __name__ == '__main__':
    # Gets a table of your private registry objects
    registry().get_registry('https://registry.dellius.app',"dalexander","PRIVATE_REGISTRY_AUTH")