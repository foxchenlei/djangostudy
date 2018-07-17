# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('asset_type', models.CharField(verbose_name='资产类型', max_length=64, default='server', choices=[('server', '服务器'), ('networkdevice', '网络设备'), ('storagedevice', '存储设备'), ('securitydevice', '安全设备'), ('software', '软件资产')])),
                ('name', models.CharField(verbose_name='资产名称', max_length=64, unique=True)),
                ('sn', models.CharField(verbose_name='资产序列号', max_length=128, unique=True)),
                ('status', models.SmallIntegerField(verbose_name='设备状态', default=0, choices=[(0, '在线'), (1, '下线'), (2, '未知'), (3, '故障'), (4, '备用')])),
                ('manage_ip', models.GenericIPAddressField(verbose_name='管理IP', null=True, blank=True)),
                ('purchase_day', models.DateField(verbose_name='购买日期', null=True, blank=True)),
                ('expire_day', models.DateField(verbose_name='过保日期', null=True, blank=True)),
                ('price', models.FloatField(verbose_name='价格', null=True, blank=True)),
                ('memo', models.TextField(verbose_name='备注', null=True, blank=True)),
                ('c_time', models.DateTimeField(verbose_name='批准日期', auto_now_add=True)),
                ('m_time', models.DateTimeField(verbose_name='更新日期', auto_now=True)),
                ('admin', models.ForeignKey(verbose_name='资产管理员', null=True, blank=True, related_name='admin', to=settings.AUTH_USER_MODEL)),
                ('approved_by', models.ForeignKey(verbose_name='批准人', null=True, blank=True, related_name='approved_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '资产总表',
                'verbose_name_plural': '资产总表',
                'ordering': ['c_time'],
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='业务线', max_length=64, unique=True)),
                ('memo', models.CharField(verbose_name='备注', max_length=64, null=True, blank=True)),
                ('parent_unit', models.ForeignKey(null=True, blank=True, related_name='parent_level', to='cmdb.BusinessUnit')),
            ],
            options={
                'verbose_name': '业务线',
                'verbose_name_plural': '业务线',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sn', models.CharField(verbose_name='合同号', max_length=128, unique=True)),
                ('name', models.CharField(verbose_name='合同名称', max_length=64)),
                ('memo', models.TextField(verbose_name='备注', null=True, blank=True)),
                ('price', models.IntegerField(verbose_name='合同金额')),
                ('detail', models.TextField(verbose_name='合同详细', null=True, blank=True)),
                ('start_day', models.DateField(verbose_name='开始日期', null=True, blank=True)),
                ('end_day', models.DateField(verbose_name='失效日期', null=True, blank=True)),
                ('license_num', models.IntegerField(verbose_name='license数量', null=True, blank=True)),
                ('c_day', models.DateField(verbose_name='创建日期', auto_now_add=True)),
                ('m_day', models.DateField(verbose_name='修改日期', auto_now=True)),
            ],
            options={
                'verbose_name': '合同',
                'verbose_name_plural': '合同',
            },
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('cpu_model', models.CharField(verbose_name='CPU型号', max_length=128, null=True, blank=True)),
                ('cpu_count', models.PositiveSmallIntegerField(verbose_name='物理CPU个数', default=1)),
                ('cpu_core_count', models.PositiveSmallIntegerField(verbose_name='CPU核数', default=1)),
                ('asset', models.OneToOneField(to='cmdb.Asset')),
            ],
            options={
                'verbose_name': 'CPU',
                'verbose_name_plural': 'CPU',
            },
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sn', models.CharField(verbose_name='硬盘SN号', max_length=128)),
                ('slot', models.CharField(verbose_name='所在插槽位', max_length=64, null=True, blank=True)),
                ('model', models.CharField(verbose_name='磁盘型号', max_length=128, null=True, blank=True)),
                ('manufacturer', models.CharField(verbose_name='磁盘制造商', max_length=128, null=True, blank=True)),
                ('capacity', models.FloatField(verbose_name='磁盘容量(GB)', null=True, blank=True)),
                ('interface_type', models.CharField(verbose_name='接口类型', max_length=16, default='unknown', choices=[('SATA', 'SATA'), ('SAS', 'SAS'), ('SCSI', 'SCSI'), ('SSD', 'SSD'), ('unknown', 'unknown')])),
                ('asset', models.ForeignKey(to='cmdb.Asset')),
            ],
            options={
                'verbose_name': '硬盘',
                'verbose_name_plural': '硬盘',
            },
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='事件名称', max_length=128)),
                ('event_type', models.SmallIntegerField(verbose_name='事件类型', default=4, choices=[(0, '其它'), (1, '硬件变更'), (2, '新增配件'), (3, '设备下线'), (4, '设备上线'), (5, '定期维护'), (6, '业务上线\\更新\\变更')])),
                ('component', models.CharField(verbose_name='事件子项', max_length=256, null=True, blank=True)),
                ('detail', models.TextField(verbose_name='事件详情')),
                ('date', models.DateTimeField(verbose_name='事件时间', auto_now_add=True)),
                ('memo', models.TextField(verbose_name='备注', null=True, blank=True)),
                ('asset', models.ForeignKey(null=True, blank=True, to='cmdb.Asset', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': '事件纪录',
                'verbose_name_plural': '事件纪录',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='机房名称', max_length=64, unique=True)),
                ('memo', models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)),
            ],
            options={
                'verbose_name': '机房',
                'verbose_name_plural': '机房',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='厂商名称', max_length=64, unique=True)),
                ('telephone', models.CharField(verbose_name='支持电话', max_length=30, null=True, blank=True)),
                ('memo', models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)),
            ],
            options={
                'verbose_name': '厂商',
                'verbose_name_plural': '厂商',
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sub_asset_type', models.SmallIntegerField(verbose_name='网络设备类型', default=0, choices=[(0, '路由器'), (1, '交换机'), (2, '负载均衡'), (4, 'VPN设备')])),
                ('vlan_ip', models.GenericIPAddressField(verbose_name='VLanIP', null=True, blank=True)),
                ('intranet_ip', models.GenericIPAddressField(verbose_name='内网IP', null=True, blank=True)),
                ('model', models.CharField(verbose_name='网络设备型号', max_length=128, null=True, blank=True)),
                ('firmware', models.CharField(verbose_name='设备固件版本', max_length=128, null=True, blank=True)),
                ('port_num', models.SmallIntegerField(verbose_name='端口个数', null=True, blank=True)),
                ('device_detail', models.TextField(verbose_name='详细配置', null=True, blank=True)),
                ('asset', models.OneToOneField(to='cmdb.Asset')),
            ],
            options={
                'verbose_name': '网络设备',
                'verbose_name_plural': '网络设备',
            },
        ),
        migrations.CreateModel(
            name='NewAssetApprovalZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sn', models.CharField(verbose_name='资产SN号', max_length=128, unique=True)),
                ('asset_type', models.CharField(verbose_name='资产类型', null=True, default='server', blank=True, max_length=64, choices=[('server', '服务器'), ('networkdevice', '网络设备'), ('storagedevice', '存储设备'), ('securitydevice', '安全设备'), ('IDC', '机房'), ('software', '软件资产')])),
                ('manufacturer', models.CharField(verbose_name='生产厂商', max_length=64, null=True, blank=True)),
                ('model', models.CharField(verbose_name='型号', max_length=128, null=True, blank=True)),
                ('ram_size', models.PositiveIntegerField(verbose_name='内存大小', null=True, blank=True)),
                ('cpu_model', models.CharField(verbose_name='CPU型号', max_length=128, null=True, blank=True)),
                ('cpu_count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('cpu_core_count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('os_distribution', models.CharField(blank=True, max_length=64, null=True)),
                ('os_type', models.CharField(blank=True, max_length=64, null=True)),
                ('os_release', models.CharField(blank=True, max_length=64, null=True)),
                ('data', models.TextField(verbose_name='资产数据')),
                ('c_time', models.DateTimeField(verbose_name='汇报日期', auto_now_add=True)),
                ('m_time', models.DateTimeField(verbose_name='数据更新日期', auto_now=True)),
                ('approved', models.BooleanField(verbose_name='是否批准', default=False)),
            ],
            options={
                'verbose_name': '新上线待批准资产',
                'verbose_name_plural': '新上线待批准资产',
                'ordering': ['c_time'],
            },
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='网卡名称', max_length=64, null=True, blank=True)),
                ('model', models.CharField(verbose_name='网卡型号', max_length=128)),
                ('mac', models.CharField(verbose_name='MAC地址', max_length=64)),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP地址', null=True, blank=True)),
                ('net_mask', models.CharField(verbose_name='掩码', max_length=64, null=True, blank=True)),
                ('bonding', models.CharField(verbose_name='绑定地址', max_length=64, null=True, blank=True)),
                ('asset', models.ForeignKey(to='cmdb.Asset')),
            ],
            options={
                'verbose_name': '网卡',
                'verbose_name_plural': '网卡',
            },
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sn', models.CharField(verbose_name='SN号', max_length=128, null=True, blank=True)),
                ('model', models.CharField(verbose_name='内存型号', max_length=128, null=True, blank=True)),
                ('manufacturer', models.CharField(verbose_name='内存制造商', max_length=128, null=True, blank=True)),
                ('slot', models.CharField(verbose_name='插槽', max_length=64)),
                ('capacity', models.IntegerField(verbose_name='内存大小(GB)', null=True, blank=True)),
                ('asset', models.ForeignKey(to='cmdb.Asset')),
            ],
            options={
                'verbose_name': '内存',
                'verbose_name_plural': '内存',
            },
        ),
        migrations.CreateModel(
            name='SecurityDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sub_asset_type', models.SmallIntegerField(verbose_name='安全设备类型', default=0, choices=[(0, '防火墙'), (1, '入侵检测设备'), (2, '互联网网关'), (4, '运维审计系统')])),
                ('asset', models.OneToOneField(to='cmdb.Asset')),
            ],
            options={
                'verbose_name': '安全设备',
                'verbose_name_plural': '安全设备',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sub_asset_type', models.SmallIntegerField(verbose_name='服务器类型', default=0, choices=[(0, 'PC服务器'), (1, '刀片机'), (2, '小型机')])),
                ('created_by', models.CharField(verbose_name='添加方式', max_length=32, default='auto', choices=[('auto', '自动添加'), ('manual', '手工录入')])),
                ('model', models.CharField(verbose_name='服务器型号', max_length=128, null=True, blank=True)),
                ('raid_type', models.CharField(verbose_name='Raid类型', max_length=512, null=True, blank=True)),
                ('os_type', models.CharField(verbose_name='操作系统类型', max_length=64, null=True, blank=True)),
                ('os_distribution', models.CharField(verbose_name='发行版本', max_length=64, null=True, blank=True)),
                ('os_release', models.CharField(verbose_name='操作系统版本', max_length=64, null=True, blank=True)),
                ('asset', models.OneToOneField(to='cmdb.Asset')),
                ('hosted_on', models.ForeignKey(verbose_name='宿主机', null=True, blank=True, related_name='hosted_on_server', to='cmdb.Server')),
            ],
            options={
                'verbose_name': '服务器',
                'verbose_name_plural': '服务器',
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sub_asset_type', models.SmallIntegerField(verbose_name='软件类型', default=0, choices=[(0, '操作系统'), (1, '办公\\开发软件'), (2, '业务软件')])),
                ('license_num', models.IntegerField(verbose_name='授权数量', default=1)),
                ('version', models.CharField(verbose_name='软件/系统版本', max_length=64, help_text='例如: CentOS release 6.7 (Final)', unique=True)),
            ],
            options={
                'verbose_name': '软件/系统',
                'verbose_name_plural': '软件/系统',
            },
        ),
        migrations.CreateModel(
            name='StorageDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sub_asset_type', models.SmallIntegerField(verbose_name='存储设备类型', default=0, choices=[(0, '磁盘阵列'), (1, '网络存储器'), (2, '磁带库'), (4, '磁带机')])),
                ('asset', models.OneToOneField(to='cmdb.Asset')),
            ],
            options={
                'verbose_name': '存储设备',
                'verbose_name_plural': '存储设备',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='标签名', max_length=32, unique=True)),
                ('c_day', models.DateField(verbose_name='创建日期', auto_now_add=True)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='eventlog',
            name='new_asset',
            field=models.ForeignKey(null=True, blank=True, to='cmdb.NewAssetApprovalZone', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(verbose_name='事件执行人', null=True, blank=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(verbose_name='所属业务线', null=True, blank=True, to='cmdb.BusinessUnit'),
        ),
        migrations.AddField(
            model_name='asset',
            name='contract',
            field=models.ForeignKey(verbose_name='合同', null=True, blank=True, to='cmdb.Contract'),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(verbose_name='所在机房', null=True, blank=True, to='cmdb.IDC'),
        ),
        migrations.AddField(
            model_name='asset',
            name='manufacturer',
            field=models.ForeignKey(verbose_name='制造商', null=True, blank=True, to='cmdb.Manufacturer'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tags',
            field=models.ManyToManyField(verbose_name='标签', to='cmdb.Tag', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='ram',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='nic',
            unique_together=set([('asset', 'model', 'mac')]),
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together=set([('asset', 'sn')]),
        ),
    ]
