from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,re

class Post (object):
    def __init__ (self, postinnerhtml,post_content):
        
        """Create a post object out of every post's HTML code."""

        self.post_content=post_content

        try:
            self.poster_fid=re.search(r'\/ajax\/hovercard\/user.php\?id\=(\d*)\&amp',postinnerhtml).group(1)
        except:
            self.poster_fid=None
            #print "error with fid, log saved"
        try:
            self.poster_name=re.search(r'alt="" aria-label="(.*)" role="img"',postinnerhtml).group(1)
        except:
            self.poster_name=None
            #print "error with name, log saved"
        try:
            self.poster_phone=re.search(r'(961\d{7,8})|(\d{7,8})|(\d{2,3}[\\\/\.\-\_\s]{1,2}\d{6,8})|((\d{2,3}[\\\/\s\-\.]){2,4}\d{2,3})',self.post_content).group()
        except:
            self.poster_phone=''
            postsfile=open ('C:/Users/Lozinsky/Desktop/pagesource.txt','a+')
            
            try:
                postsfile.write(self.post_content.encode('utf-8'))
            except:
                print 'couldnt write post content'
            postsfile.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
            postsfile.close()
            #print "error with phone, phone is none"
        
        
    def __str__ (self):
        try:
            return ''+str(self.poster_name)+','+str(self.poster_fid)+','+str(self.poster_phone)
        except:
            return ''
            print "Probably unicode error"
        
        

def scroll_down(wd,amount=50):
    for i in xrange(amount):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


def to_csv (posts_array):
    csv_file=open('C:/Users/Lozinsky/Desktop/FBparser.csv','a+')
    csv_file.write('Name,FID,Phone\n')
    for i in xrange(len(posts_array)):
        try:
            postcontent=posts_array[i].find_elements_by_css_selector('div._5pbx.userContent')[0].text
        except:
            postcontent=''
        current_post=Post(posts_array[i].get_attribute('innerHTML'),postcontent)
        if str(current_post)!='':
            csv_file.write(str(current_post)+'\n')
    csv_file.close()

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get('http://facebook.com')
    username=driver.find_element_by_css_selector('input#email.inputtext')#enter mail
    username.send_keys('mail123')
    passwd=driver.find_element_by_css_selector('input#pass.inputtext')
    passwd.send_keys('<enterpass>') #enter pass
    passwd.send_keys(Keys.RETURN)
    driver.get('http://facebook.com/<enter group>') #enter group
    scroll_down(driver)
    posts=driver.find_elements_by_css_selector('div._5pcr.fbUserPost')
    print 'len of posts= '+str(len(posts))
    to_csv(posts)


    print 'finished!'
