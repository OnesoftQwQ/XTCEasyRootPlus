import os
from rich.console import Console
from rich.text import Text
from time import sleep
import wget
import json
import urllib.error
import tools
import subprocess
import sys
import zipfile
import noneprompt
import requests
from rich.console import Console
from rich.table import Column,Table
import shutil
import threading

version = [0,2,'b']

os.system(f'title XTCEasyRootPlus v{version[0]}.{version[1]}')
console = Console()
status = console.status('')
print = console.print

if not os.path.exists('tmp/'):
    os.mkdir('tmp')
else:
    for i in os.listdir('tmp'):
        if os.path.isfile(f'tmp/{i}'):
            os.remove(f'tmp/{i}')
        else:
            shutil.rmtree(f'tmp/{i}')


if not os.path.exists('data/'):
    os.mkdir('data')

if len(version) == 3 and version[2] == 'b':
    print('[red][!][/red]警告:这是一个测试版本,非常不稳定,若非测试人员请勿使用!')
    sleep(5)

#检查更新
os.system('cls')
status.update('正在检查更新')
status.start()
console.log('检查最新版本')
try: #尝试获取版本文件
    r = requests.get('https://xtc-files.oss.onesoft.top/easyrootplus/version.json')   #获取版本信息
    read = json.loads(r.content)
    latest_version = read
    if latest_version[0] >= version[0] and latest_version[1] > version[1]:
        console.log(f'发现新版本:{latest_version[0]}.{latest_version[1]}')
        console.log('开始下载新版本......')
        status.update('下载新版本')
        tools.download_file('https://xtc-files.oss.onesoft.top/easyrootplus/XTCEasyRootPlusInstaller.exe','tmp/XTCEasyRootPlusInstaller.exe')
        subprocess.Popen('tmp/XTCEasyRootPlusInstaller.exe')
        sys.exit()
except requests.ConnectionError:   #捕捉下载失败错误
    console.log('检查更新失败，请检查你的网络或稍后再试')
    status.stop()
    tools.exit_after_enter() #退出

console.log('当前版本为最新!')
sleep(1)

while True:
    #清屏并停止状态指示
    status.stop()
    os.system('cls')

    #主菜单
    tools.print_logo(version)
    print(f'\nXTCEasyRootPlus [blue]v{version[0]}.{version[1]}[/blue]')
    print('本软件是[green]免费公开使用[/green]的，如果你是付费买来的请马上退款，你被骗了！\n')
    choice = noneprompt.ListPrompt(
        '请选择功能',
        [
            noneprompt.Choice('1.一键Root'),
            noneprompt.Choice('2.超级恢复(救砖/降级)'),
            noneprompt.Choice('3.工具箱'),
            noneprompt.Choice('4.关于')
        ]
    ).prompt()


    if choice.name == '1.一键Root':
        console.rule('免责声明',characters='=')
        print('''如您使用[red]Sky iMoo[/red]相关文件(包括但不限于任意出自本群文件或其他来源的Magisk模块，root文件等)对手表进行了ROOT或安装非官方商城应用，即代表您默认同意本《免责声明》
1.使用Sky iMoo提供的文件后，您的设备将不再为原厂固件，可能[red]无法正常使用[/red]由广东小天才科技有限公司提供的服务，且小天才无需无理由恢复这些功能。
2.使用Sky iMoo提供的文件后导致的家长端等功能出现[red]任何异常[/red](包括但不限于文件错误)，Sky iMoo及管理组无需承担任何责任。
3.您需要[red]自觉[/red]使用网络，如您因沉迷于网络导致身心健康受损或学习成绩下降等，Sky iMoo及管理组无需承担任何责任。
4.在刷入非官方固件后您的设备可能会[red]失去保修[/red]，尽管您的设备可以恢复到官方固件。
5.您对手表进行解除第三方软件安装限制之操作属于您的[red]自愿[/red]行为，Sky iMoo及管理组并没有主动要求他人进行ROOT，解除安装限制。
6.Sky iMoo并[red]不提供 手表强制解绑 服务[/red]，如您捡拾他人的手表，请自觉联系当地110归还失主。手表解绑属于非法行为，请归还失主。而不要尝试通过ROOT等刷机手段解除挂失锁。
7.Sky iMoo只提供于ROOT有关的文件，Sky iMoo及管理组无需承担任何责任。
8.如果您帮助他人或教唆他人ROOT或解除第三方软件安装限制，对他人手表进行一切可能有损坏的操作需[red]由机主本人同意[red]并由机主自行操作，责任由机主自行承担。
9.[red]禁止恶意损坏他人财产[/red]，如您在ROOT或解除第三方软件安装限制后恶意使用他人信息未经授权操作他人账号而导致的他人出现任何财产损失，Sky iMoo及管理组无需承担任何责任，责任由您自行承担。
10.当《免责声明》发生任何变动时均认为您[red]默认同意[/red]修改后的内容。''')
        console.rule('免责声明',characters='=')
        confirm = noneprompt.ConfirmPrompt('你是否已阅读并同意本《免责声明》',default_choice=False).prompt()
        if not confirm:
            print('[red][!][/red] 由于你不同意本声明，程序将退出')
            print('按下回车退出')
            tools.exit_after_enter()
        input('请拔出手表上的SIM卡,拔出后按下回车下一步')
        adb = tools.ADB('bin/adb.exe')
        print('\r',end='')
        status.update("等待设备连接")
        status.start()
        print('请在手表上打开并用数据线将手表连接至电脑')
        adb.wait_for_connect()

        console.log('设备已连接')
        status.update('获取设备信息')
        console.log('获取设备信息')
        info = adb.get_info()
        table = Table()
        table.add_column("型号", width=12)
        table.add_column("代号")
        table.add_column("系统版本", justify="right")
        table.add_column("安卓版本", justify="right")
        table.add_row(info['model'],info['innermodel'],info['version_of_system'],info['version_of_android'])
        print(table)
        status.stop()
        if not info['innermodel'] in tools.xtc_models.keys():
            print('你的设备貌似不是小天才设备,或者还没被支持,目前暂不支持一键Root')
            print('按下回车键退出')
            tools.exit_after_enter()
        elif tools.xtc_models[info['innermodel']] == 'Z10':
            print('Z10不支持Root!')
            print('按下回车退出')
            tools.exit_after_enter()

        model = tools.xtc_models[info['innermodel']]

        choice = noneprompt.ListPrompt(
            '请选择想要的Magisk版本',
            choices=[
                noneprompt.Choice('1.Magisk25200'),
                noneprompt.Choice('2.MagiskDelta25210')
            ],
        ).prompt()
        if choice.name == '1.Magisk25200':
            magisk = '25200'
        elif choice.name == '2.MagiskDelta25210':
            magisk = '25210'

        if not os.path.exists(f'data/{model}'):
            console.log('下载文件')
            status.update('下载文件')
            tools.download_file(f'https://xtc-files.oss.onesoft.top/easyrootplus/{model}.zip',f'tmp/{model}.zip')
            
            console.log('解压文件')
            status.update('解压文件')
            tools.extract_all(f'tmp/{model}.zip',f'data/{model}/')
        
        if magisk == '25200':
            tools.download_file('https://xtc-files.oss.onesoft.top/easyrootplus/1userdata.img','tmp/userdata.img')
        elif magisk == '25210':
            tools.download_file('https://xtc-files.oss.onesoft.top/easyrootplus/2userdata.img','tmp/userdata.img')
        
        status.stop()
        
        def download_all_files():
            if info['version_of_android'] == '7.1.1':
                filelist = ['appstore.apk','moyeinstaller.apk','xtctoolbox.apk','filemanager.apk','notice.apk']
                for i in filelist:
                    tools.download_file(f'https://xtc-files.oss.onesoft.top/easyrootplus/apps/{i}',f'tmp/{i}',progress=False)
            elif info['version_of_android'] == '8.1.0':
                filelist = ['appstore.apk','notice.apk','wxzf.apk','wcp2.apk','datacenter.apk','xws.apk','launcher.apk','11605.apk','filemanager.apk','settings.apk']
                for i in filelist:
                    tools.download_file(f'https://xtc-files.oss.onesoft.top/easyrootplus/apps/{i}',f'tmp/{i}',progress=False)
                tools.download_file(f'https://xtc-files.oss.onesoft.top/easyrootplus/xtcpatch/{model}.zip','tmp/xtcpatch.zip')

        download_thread = threading.Thread(target=download_all_files)
        download_thread.start()

        if info['version_of_android'] == '7.1.1':
            choice = noneprompt.ListPrompt(
                '请选择Root方案',
                choices=[
                    noneprompt.Choice('1.boot方案(如果你已经降级选这个)'),
                    noneprompt.Choice('2.recovery方案(如果你没有用过超级恢复/降级选这个)')
                ]
                ).prompt()
            if choice.name == '1.boot方案(如果你已经降级选这个)':
                mode = 'boot'
            elif choice.name == '2.recovery方案(如果你没有用过超级恢复/降级选这个)':
                mode = 'recovery'
        

        while True:
            confirm = noneprompt.ConfirmPrompt('你是否已经将SIM卡拔出?',default_choice=False).prompt()
            if confirm:
                break
            else:
                print('请将SIM卡拔出!')
        while True:
            confirm = noneprompt.ConfirmPrompt('请确认你已经将SIM卡拔出!否则若Root后出现「手表验证异常」我们概不负责!',default_choice=False).prompt()
            if confirm:
                break
            else:
                print('请将SIM卡拔出!')
        
        output,err = adb.shell('getprop gsm.xtcplmn.plmnstatus')
        if '没有服务' in output:
            status.stop()
            input('手表状态:无服务,请确定您已拔卡!如果不想喜提「手表验证异常」请先拔卡,如已拔卡无视此提示')
        elif '只能拨打紧急电话' in output:
            status.stop()
            input('您似乎没有拔卡!如果不想喜提「手表验证异常」请先拔卡,如已拔卡无视此提示')

        if info['version_of_android'] == '7.1.1':
            status.update('重启设备至9008模式')
            status.start()
            console.log('重启设备至9008模式')
            adb.adb('reboot edl')
            console.log('等待连接')
            port = tools.wait_for_edl()

            console.log('连接成功,开始读取boot分区')
            status.update('读取boot分区')
            qt = tools.QT('bin/QSaharaServer.exe','bin/fh_loader.exe',port,f'data/{model}/mbn.mbn')
            tools.iferror(qt.intosahara(),'进入sahara模式',status,mode='skip')
            tools.iferror(qt.load_xml(f'data/{model}/boot.xml'),'读取boot分区',status,mode='exit9008',qt=qt)

            console.log('读取boot分区成功!')
            shutil.copy('boot.img','tmp/')
            os.remove('boot.img')

            console.log('开始修补boot分区')
            status.update('修补boot分区')
            tools.patch_boot('bin/magiskboot.exe','tmp/boot.img','bin/20400.zip','tmp/',console)
            console.log('修补完毕')

            if mode == 'boot':
                console.log('重新刷入boot')
                status.update('刷入boot')
                os.remove('tmp/boot.img')
                os.rename('tmp/boot_new.img','tmp/boot.img')
                tools.iferror(qt.fh_loader_err(rf'--port=\\.\COM{port} --memoryname=emmc --search_path=tmp/ --sendxml=data/{model}/boot.xml --noprompt'),'刷入boot分区',status,mode='exit9008',qt=qt)

            elif mode == 'recovery':
                console.log('刷入recovery')
                status.update('刷入recovery')
                os.rename('tmp/boot_new.img','tmp/recovery.img')
                tools.iferror(qt.fh_loader_err(rf'--port=\\.\COM{port} --memoryname=emmc --search_path=tmp/ --sendxml=data/{model}/recovery.xml --noprompt'),'刷入recovery',status,mode='exit9008',qt=qt)

                console.log('刷入misc')
                status.update('刷入misc')
                tools.iferror(qt.fh_loader_err(rf'--port=\\.\COM{port} --memoryname=emmc --search_path=data/{model}/ --sendxml=data/{model}/misc.xml --noprompt'),'刷入misc',status,mode='exit9008',qt=qt)

            console.log('刷入成功,退出9008模式')
            status.update('退出9008')
            tools.iferror(qt.exit9008(),'退出9008模式',status,mode='stop')

            console.log('等待重新连接')
            status.update('等待重新连接')
            adb.wait_for_connect()
            adb.wait_for_complete()

            console.log('安装Magisk管理器')
            status.update('安装Magisk管理器')
            tools.iferror(adb.install(f'data/{model}/manager.apk'),'安装Magisk管理器',status,mode='stop')

            console.log('启动管理器')
            status.update('启动管理器')
            sleep(5)
            adb.shell('am start com.topjohnwu.magisk/a.c')
            adb.push(f'data/{model}/xtcpatch','/sdcard/')
            adb.push(f'data/{model}/magiskfile','/sdcard/')
            adb.push('bin/2100.sh','/sdcard/')
            console.log('刷入模块')
            status.update('刷入模块')
            adb.shell('su -c sh /sdcard/2100.sh')
            adb.install_module('bin/xtcpatch2100.zip')
            adb.shell('rm -rf /sdcard/xtcpatch /sdcard/magiskfile /sdcard/2100.sh')

            if download_thread.is_alive():
                console.log('下载文件')
                status.update('下载文件')
                download_thread.join()

            console.log('安装必备软件')
            status.update('安装必备软件')
            for i in os.listdir(f'tmp/'):
                if i[-3:] == 'apk':
                    tools.iferror(adb.install(f'tmp/{i}',[]),f'安装{i}',status,mode='skip')

            if mode == 'recovery':
                console.log('重启设备至9008模式')
                status.update('等待连接')
                adb.adb('reboot edl')
                port = tools.wait_for_edl()

                console.log('进入sahara模式')
                status.update('进入sahara模式')
                tools.iferror(qt.intosahara(),'进入sahara模式',status,mode='stop')

                console.log('刷入recovery')
                status.update('刷入recovery')
                tools.iferror(qt.fh_loader_err(rf'--port=\\.\COM{port} --memoryname=emmc --search_path=tmp/ --sendxml=data/{model}/recovery.xml --noprompt'),'刷入recovery',status,mode='exit9008',qt=qt)

                console.log('刷入misc')
                status.update('刷入misc')
                tools.iferror(qt.fh_loader_err(rf'--port=\\.\COM{port} --memoryname=emmc --search_path=data/{model}/ --sendxml=data/{model}/misc.xml --noprompt'),'刷入misc',status,mode='exit9008',qt=qt)

                console.log('退出9008模式')
                status.update('等待重新连接')
                tools.iferror(qt.exit9008(),'退出9008模式',status,mode='stop')

                adb.wait_for_connect()
                adb.wait_for_complete()

            # console.log('安装Xposed')
            # status.update('安装Xposed')
            # adb.install_module('bin/xposed-magisk.zip')
            # console.log('重启设备')
            # console.log('提示:首次刷入Xposed后开机可能需要[bold]7-15分钟[/bold],请耐心等待')
            # status.update('等待重新连接')
            # adb.adb('reboot')
            # adb.wait_for_connect()
            # adb.wait_for_complete()
            # console.log('连接成功')

            # status.update('设置充电可用')
            # console.log('设置充电可用')
            # adb.shell('setprop persist.sys.charge.usable true')

            # console.log('充电可用已开启')
            # console.log('模拟未充电状态')
            # status.update('模拟未充电状态')
            # adb.shell('dumpsys battery unplug')
            # console.log('已模拟未充电状态')
            # status.stop()

            # console.rule('接下来需要你对手表进行一些手动操作',characters='=')
            # input('请打开手表上的"Xposed Installer"应用,点击左上角的三条杠,点击"模块",勾选"核心破解"选项\n完成操作后请按回车继续')
            # console.rule(characters='=')

            # status.update('等待重新连接')
            # status.start()
            # console.log('重启手表')
            # adb.adb('reboot')
            # adb.wait_for_connect()
            # adb.wait_for_complete()

            # console.log('连接成功!')
            # status.update('安装改版系统应用')
            # console.log('开始安装改版系统应用')
            # for i in os.listdir('bin/sysapps/'):
            #     tools.iferror(adb.install(f'bin/sysapps/{i}'),f'安装{i}',status,mode='skip')

            status.stop()
            # console.log('恭喜你,你的手表ROOT完毕!')
            input('恭喜你,Root成功!按回车返回主界面')




        elif info['version_of_android'] == '8.1.0':
            is_v3 = tools.is_v3(model,info['version_of_system'])
            status.update('等待连接') 
            status.start()
            console.log('重启设备至9008模式')
            adb.adb('reboot edl')
            console.log('等待连接')
            port = tools.wait_for_edl()
            
            console.log('连接成功')
            console.log('开始读取boot分区')
            status.update('读取boot分区') 
            qt = tools.QT('bin/QSaharaServer.exe','bin/fh_loader.exe',port,'bin/msm8937.mbn')
            tools.iferror(qt.intosahara(),'进入sahara模式',status,mode='stop')
            tools.iferror(qt.load_xml(f'data/{model}/boot.xml'),'读取boot分区',status,mode='exit9008',qt=qt)
            
            console.log('读取boot分区成功!')
            shutil.copy('boot.img','tmp/')
            os.remove('boot.img')
            
            console.log('开始修补boot分区')
            status.update('修补boot分区') 
            tools.patch_boot('bin/magiskboot.exe','tmp/boot.img',f'bin/{magisk}.apk','tmp/',console)
            
            console.log('修补完毕')
            if model == 'Z7A' or model == 'Z6_DFB':
                console.log('刷入recovery')
                status.update('刷入recovery') 
                os.rename('tmp/boot_new.img','recovery.img')
                tools.iferror(qt.fh_loader_err(rf'--port=\\.\COM{port} --memoryname=emmc --search_path=tmp/ --sendxml=data/{model}/recovery.xml --noprompt'),'刷入recovery',status,mode='exit9008',qt=qt)
            elif not is_v3:
                console.log('刷入boot')
                status.update('刷入boot') 
                os.remove('tmp/boot.img')
                os.rename('tmp/boot_new.img','boot.img')
                tools.iferror(qt.fh_loader_err(rf'--port=\\.\COM{port} --memoryname=emmc --search_path=tmp/ --sendxml=data/{model}/boot.xml --noprompt'),'刷入boot',status,mode='exit9008',qt=qt)
            console.log('刷入boot,aboot,userdata,misc')
            status.update('刷入boot,aboot,userdata,misc') 
            tools.iferror(qt.fh_loader_err(rf'--port=\\.\COM{port} --memoryname=emmc --search_path=data/{model}/ --sendxml=data/{model}/rawprogram0.xml --noprompt'),'刷入rawprogram',status,mode='stop')
            console.log('刷入成功!')
            if is_v3:
                status.update('刷入空boot') 
                console.log('刷入空boot')
                os.remove('tmp/boot.img')
                shutil.copy(f'bin/eboot.img','tmp/boot.img')
                tools.iferror(qt.fh_loader_err(rf'--port=\\.\COM{port} --memoryname=emmc --search_path=tmp/ --sendxml=data/{model}/rawprogram0.xml --noprompt'),'刷入空boot',status,mode='exit9008',qt=qt)
            tools.iferror(qt.exit9008(),'退出9008模式',status,mode='stop')
            status.update('退出9008')
            console.log('退出9008模式')
            status.update('等待重新连接') 
            fastboot = tools.FASTBOOT('bin/fastboot.exe')
            if not model in ('Z7A','Z6_DFB'):
                if is_v3:
                    fastboot.wait_for_fastboot()
                    status.update('刷入boot') 
                    console.log('刷入boot')
                    tools.iferror(fastboot.flash('boot','tmp/boot_new.img'),'刷入boot',status,mode='stop')
                else:
                    adb.wait_for_connect()
                    adb.wait_for_complete()
                    adb.adb('reboot bootloader')
                    fastboot.wait_for_fastboot()
                status.update('刷入userdata') 
                console.log('刷入userdata')
                tools.iferror(fastboot.flash('userdata','tmp/userdata.img'),'刷入userdata',status)
                status.update('刷入misc') 
                console.log('刷入misc')
                with open('tmp/misc.bin','w') as f:
                    f.write('ffbm-02')
                tools.iferror(fastboot.flash('misc','tmp/misc.bin'),'刷入misc',status)
                fastboot.fastboot('reboot')
                status.update('等待重新连接') 
                console.log('刷入完毕,重启进入系统')
            adb.wait_for_connect()
            adb.wait_for_complete()
            console.log('连接成功')
            if is_v3:
                console.log('创建空文件')
                status.update('创建空文件')
                adb.shell('mkdir /data/adb/modules/XTCPatch/system/app/XTCLauncher')
                adb.shell('touch /data/adb/modules/XTCPatch/system/app/XTCLauncher/XTCLauncher.apk')
                console.log('重启设备')
                status.update('等待重新连接')
                adb.adb('reboot')
                adb.wait_for_connect()
                adb.wait_for_complete()
                console.log('连接成功!')
                if download_thread.is_alive():
                    console.log('下载文件')
                    status.update('下载文件')
                    download_thread.join()
                console.log('安装11605桌面')
                status.update('安装桌面')
                tools.iferror(adb.install('bin/11605launcher.apk'),'安装11605桌面',status,mode='stop')
                console.log('重启设备')
                status.update('等待连接')
                adb.adb('reboot')
                adb.wait_for_connect()
                adb.wait_for_complete()

            if not model in ('Z7A','Z6_DFB'):
                status.update('等待连接') 
                console.log('重启进入Fastboot')
                adb.adb('reboot bootloader')
                fastboot.wait_for_fastboot()
                status.update('擦除misc') 
                console.log('擦除misc')
                fastboot.erase('misc')
                status.update('等待重新连接') 
                console.log('刷入完毕,重启进入系统')
                console.log('提示:若已进入系统但仍然卡在这里,请打开拨号盘输入"*#0769651#*"手动开启adb')
                fastboot.fastboot('reboot')
                adb.wait_for_connect()
                adb.wait_for_complete()

            # choice = noneprompt.ListPrompt('现在您的手表处于什么状态?',choices=[noneprompt.Choice('1.已正常开机'),noneprompt.Choice('2.仍处于黑屏状态')]).prompt()
            # if choice.name == '2.仍处于黑屏状态':
            #     pass
            console.log('开启充电可用')
            status.update('开启充电可用')
            adb.shell('setprop persist.sys.charge.usable true')
            console.log('模拟未充电')
            status.update('模拟未充电')
            adb.shell('dumpsys battery unplug')
            status.stop()

            console.rule('接下来需要你进行一些手动操作',characters='=')
            print('请完成激活向导,当提示绑定时直接右滑退出,完成开机向导,进入主界面')
            print('提示:请不要断开手表与电脑的连接!')
            print('提示:如果提示系统已被Root不用在意,没事的,点击我知道了就行')
            input('如果你已经进入主界面,请按回车进行下一步')
            console.rule('',characters='=')

            status.update('设置DPI')
            status.start()
            console.log('设置DPI为200')
            adb.shell('wm density 200')
            console.log('检测桌面是否崩溃')
            status.update('检测桌面是否崩溃')
            sleep(5)
            if not 'com.xtc.i3launcher' in adb.get_activity():
                console.log('检测到桌面崩溃!设置DPI为280')
                status('设置DPI')
                adb.shell('wm density 280')
                console.log('请点击屏幕上的"重新打开应用"')
                status.update('等待点击')
                while True:
                    if 'com.xtc.i3launcher' in adb.get_activity():
                        break
                    sleep(0.5)
            
            status.stop()
            console.rule('接下来需要你进行一些手动操作',characters='=')
            input('请打开手表上的"Magisk"或"MagiskDelta"APP,点击右上角设置,往下滑找到自动响应,将其设置为"允许";然后找到"超级用户通知",将其设置为"无",完成后按下回车继续')
            input('请打开手表上的"Edxposed Installer"APP,然后直接返回退出,完成后按下回车继续')
            input('请打开手表上的"SystemPlus"APP,依次点击"激活SystemPlus"和"激活核心破解"按钮,完成后按下回车继续')
            console.rule('',characters='=')

            adb.push('bin/systemplus.sh','/sdcard/')
            while True:
                status.update('检查SystemPlus状态')
                status.start()
                console.log('检查SystemPlus状态')
                output,err = adb.shell('sh /sdcard/systemplus.sh')
                if not '1' in output:
                    break
                else:
                    status.stop()
                    input('SystemPlus未激活!请重新按照上文提示激活!完成后按下回车继续')
            adb.shell('rm -rf /sdcard/systemplus.sh')
            console.log('SystemPlus激活成功!')

            adb.push('bin/toolkit.sh','/sdcard/')
            while True:
                status.update('检查核心破解状态')
                status.start()
                console.log('检查核心破解状态')
                output,err = adb.shell('sh /sdcard/toolkit.sh')
                if not '1' in output:
                    break
                else:
                    status.stop()
                    input('核心破解未激活!请重新按照上文提示激活!完成后按下回车继续')
            adb.shell('rm -rf /sdcard/toolkit.sh')
            console.log('核心破解激活成功!')

            console.log('重启设备')
            status.update('等待重新连接')
            adb.adb('reboot')
            adb.wait_for_connect()
            adb.wait_for_complete()

            console.log('获取uid')
            status.update('获取uid')
            chown = adb.shell('"dumpsys package com.solohsu.android.edxp.manager | grep userId="')[0].replace('\n','').replace('\r','').split('=')[1][-5:]
            console.log('更改文件所有者')
            status.update('更改文件所有者')
            adb.shell(f'"su -c chown {chown} /data/user_de/0/com.solohsu.android.edxp.manager/conf/enabled_modules.list"')
            adb.shell(f'"su -c chown {chown} /data/user_de/0/com.solohsu.android.edxp.manager/conf/modules.list"')

            if download_thread.is_alive():
                console.log('下载文件')
                status.update('下载文件')
                download_thread.join()

            console.log('安装XTCPatch')
            status.update('安装XTCPatch')
            adb.push('tmp/xtcpatch.zip','/sdcard/')
            adb.shell('su -c magisk --install-module /sdcard/xtcpatch.zip')
            adb.shell('rm -rf /sdcard/xtcpatch.zip')

            console.log('安装修改版桌面')
            status.update('安装修改版桌面')
            tools.iferror(adb.install('tmp/launcher.apk'),'安装修改版桌面',status,mode='stop')

            console.log('安装软件')
            status.update('安装软件')
            for i in ['notice.apk','wxzf.apk','appstore.apk','wcp2.apk','datacenter.apk','xws.apk','filemanager.apk','settings.apk']:
                status.update(f'安装{i}')
                tools.iferror(adb.install(f'tmp/{i}'),f'安装{i}')
            
            console.log('设置DPI为320')
            status.update('设置DPI')
            adb.shell('wm density 320')

            console.log('重启设备')
            status.update('等待连接')
            adb.adb('reboot')
            adb.wait_for_connect()
            adb.wait_for_complete()

            console.log('连接成功!')
            status.stop()
            input('恭喜你,Root成功!按回车返回主界面')
    elif choice.name== '3.工具箱':
            choice = noneprompt.ListPrompt(
            '请选择功能',
            [
                noneprompt.Choice('1.adb安装应用'),
                noneprompt.Choice('2.安装magisk模块'),
                noneprompt.Choice('3.打开充电可用'),
                noneprompt.Choice('4.')
            ]
        ).prompt()
    elif choice.name == '4.关于':
        os.system('cls')
        tools.print_logo(version)

        about = '''XTCEasyRootPlus时一个使用Python制作的小天才电话手表一键Root程序
本项目以GPL协议开源在Github:https://www.github.com/OnesoftQwQ/XTCEasyRootPlus

作者:
    [red]花火玩偶[/red] 和 [blue]Onesoft[/blue]

特别鸣谢:
    早茶光: 制作了XTCEasyRoot,xtcpatch,810和711的adbd,多个版本的改版桌面,并且为我解答了许多问题,本项目的逻辑基本上是参考[strike](抄)[/strike]的XTCEasyRoot
    huanli233: 制作了部分改版桌面,notice,systemplus,weichatpro2
'''
        
        for i in about.splitlines():
            print(i)
            sleep(0.5)

        input('按回车回到主界面......')