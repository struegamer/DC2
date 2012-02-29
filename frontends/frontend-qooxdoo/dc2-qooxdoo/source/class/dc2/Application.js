/* *******************************************************************************

   (DC)² - DataCenter Deployment Control
   Copyright (C) 2010, 2011  Stephan Adig <sh@sourcecode.de>
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation, Inc.,
   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
********************************************************************************* */


/* ************************************************************************
#asset(dc2/*)
************************************************************************ */

/**
 * This is the main application class of your custom application "dc2-frontend-qooxdoo"
 */
qx.Class.define("dc2.Application",
{
  extend : qx.application.Standalone,



  /*
  *****************************************************************************
     MEMBERS
  *****************************************************************************
  */

    members : {
      cs2_main:null,
      xen_main:null,
    /**
     * This method contains the initial application code and gets called 
     * during startup of the application
     * 
     * @lint ignoreDeprecated(alert)
     */
        _tabView:null,
        _tabPages:{},
        _this:this,
        main : function()
        {
            // Call super class
            this.base(arguments);

            // Enable logging in debug variant
            if (qx.core.Environment.get("qx.debug"))
            {
                qx.log.appender.Native;
                qx.log.appender.Console;
            }
            this.cs2_main=new cs2.frontend.Main();
            this.xen_main=new dc2.xen.Main();
            this._createMainLayout()
        },
        _createMainLayout:function() {
            var scroller=new qx.ui.container.Scroll();
            var container=new qx.ui.container.Composite(new qx.ui.layout.Dock());
            scroller.add(container);
            this.getRoot().add(scroller,{edge:0});
            container.add(this._createContentLayout());
        },
        _createContentLayout:function() {
            var container=new qx.ui.container.Composite(new qx.ui.layout.Dock()).set({
            decorator:"main",
            allowGrowY:true
            });
            var _logo=this._createLogoLayout();
            this._tabView=new qx.ui.tabview.TabView();
            container.add(_logo,{edge:'north'});
            container.add(this._createMenuBar(),{edge:'north'});
            container.add(this._tabView,{edge:'north'});           
            return(container);
        },
        _createLogoLayout:function() {
            var logo=new qx.ui.basic.Image("dc2/logo/dc2-logo.png");
            logo.setMarginTop(logo.getMarginTop()+5);
            logo.setMarginBottom(logo.getMarginBottom()+5);
            return(logo);
        },
        _createMenuBar:function() {          
            var mainMenuHash={
                items: [
                {
                    name: "Inventory",
                    type: "menu",
                    items: [
                            {
                              name: "Hardware",
                              icon:null,
                              type:"submenu",
                              items:[
                                     { 
                                       name: "Servers",
                                       icon: "dc2/icons/16x16/server.png",
                                       type: "button",
                                       callback: this._showInventoryServers,
                                       context: this
                                     },
                                     {
                                       name: "XenServer Management",
                                       icon: "dc2/icons/16x16/xenserver.png",
                                       type: "submenu",
                                       items:[
                                             {
                                               name:"Xen Hosts",
                                               icon:null,
                                               type:"button",
                                               callback:this._showInventoryXenServer,
                                               context:this                                               
                                             },
                                             {
                                               type:"separator"
                                             },
                                             {
                                               name:"Manage Xen Virtual Machines",
                                               icon:null,
                                               type:"button",
                                               callback:this._showInventoryManageVMs,
                                               context:this
                                             }
                                       ]
                                     }
                                     ]
                            },
                            {
                              type:"separator"
                            },
                            {
                              name: "Software",
                              icon:null,
                              type:"submenu",
                              items:[
                                     {
                                       name: "Hosts",
                                       icon: "dc2/icons/16x16/hosts.png",
                                       type: "button",
                                       callback: this._showDeploymentHosts,
                                       context: this
                                     }
                              ]
                            },
                            {
                              type:"separator"
                            },                            
                    {
                        name: "Network",
                        icon: "dc2/icons/16x16/network.png",
                        type: "button",
                        callback: this._showInventoryNetworks,
                        context: this
                    }
                    ]
                },
                {
                    name: "Deployment",
                    type:"menu",
                    items: [
                            {
                              name:"Deployment State",
                              icon:null,
                              type:"button",
                              callback:this._showDeploymentInstallState,
                              context:this
                            },
                            {
                              type: "separator"
                            }
                    ]
                },
                {
                  name:"CS²",
                  type:"menu",
                  items:[
                         {                            
                            name:"Host Keys",
                            icon:null,
                            type:"button",
                            callback:this._cs2_mnuHostKeys,
                            context:this
                          },
                          {
                            type:"separator"
                          },                     
                          {
                            name:"Certification Signing Requests",
                            icon:null,
                            type:"button",
                            callback:this._cs2_mnuCSRs,
                            context:this
                          },
                          {
                            type:"separator"
                          },
                          {
                            name:"Certificates",
                            icon:null,
                            type:"button",
                            callback:this._cs2_mnuCerts,
                            context:this
                          },
                          {
                            type:"separator"
                          },
                          {
                            name:"Certificate Revokation List",
                            icon:null,
                            type:"button",
                            callback:this._cs2_mnuCrls,
                            context:this
                          },
                          {
                            type:"separator"
                          },
                          {
                            name:"ISO 3166 Country List",
                            icon:null,
                            type:"button",
                            callback:this._cs2_mnuISO3166List,
                            context:this
                          }
                         ]
                },             
                {
                    name: "Configuration",
                    type: "menu",
                    items: [
                    {        
                      name: "Authentication/Authorization",
                      type:"submenu",
                      items:[
                             {
                               name:"Users",
                               icon:null,
                               type:"button",
                               callback:this._showConfigurationUsers,
                               context:this                               
                             },
                             {
                               name:"Groups",
                               icon:null,
                               type:"button",
                               callback:this._showConfigurationGroups,
                               context:this
                             }
                             ]
                    }, 
                    
                    {
                        name: "Settings",
                        type: "submenu",
                        items: [
                        {
                            name: "Environments",
                            icon: null,
                            type: "button",
                            callback: this._showConfigurationSettingsEnvironments,
                            context: this
                        },
                        {
                          type:"separator"
                        },                        
                        {
                            name: "Default Classes",
                            icon: null,
                            type: "button",
                            callback: this._showConfigurationSettingsDefaultClasses,
                            context: this
                        },
                        {
                          name: "Class Templates",
                          icon:null,
                          type: "button",
                          callback: this._showConfigurationSettingsClassTemplates,
                          context: this
                        },
                        {
                          name:"Default Systemusers",
                          icon:null,
                          type:"button",
                          callback: this._showConfigurationSettingsSystemUsers,
                          context:this
                        },
                        {
                          name:"Default Systemgroups",
                          icon:null,
                          type:"button",
                          callback:this._showConfigurationSettingsSystemGroups,
                          context:this
                        },
                        {
                          type:"separator"
                        },
                        {
                          name:"PXE Boot Methods",
                          icon:null,
                          type:"button",
                          callback:this._showConfigurationSettingsBootMethods,
                          context:this
                        }

                        ]
                    },
                    {
                      type:"separator"
                    },
                    {
                      name:"Preferences",
                      type:"button",
                      icon:null,
                      callback: this._showConfigurationPreferences,
                      context:this
                    }
                    ]
                }                            
                ]
            };
            var _mainMenuObj=new menucreator.MenuCreator();
            var _mainMenu=_mainMenuObj.getMenuBar(mainMenuHash);
            return(_mainMenu);
        },
        _addTabPage:function(page_identifier,page_name,page_layout) {
            if (page_identifier in this._tabPages !== true) {
                var page=new qx.ui.tabview.Page(page_name);
                page.setShowCloseButton(true);
                page.setLayout(new qx.ui.layout.VBox(5));
                page.add(page_layout);
                this._tabPages[page_identifier]=page;
                this._tabView.add(page);
                this._tabView.setSelection([page]);
                this._tabPages[page_identifier].addListener("close",this._closeTabPageEvent,this);
            }
        },
        _showInventoryServers:function(e) {            
            if ("inventory_server" in this._tabPages) {
                this._tabView.setSelection([this._tabPages["inventory_server"]]);
            } else {
                var server_tbl=new dc2.models.Servers(dc2.helpers.BrowserCheck.RPCUrl(false));
                var server_search_dlg=new dc2.dialogs.search.Servers();               
                var server_edit_dialog=new dc2.dialogs.EditServer();
                var server_table_options={
                    enableAddEntry:false,
                    enableEditEntry:true,
                    enableDeleteEntry:true,
                    enableReloadEntry:true,                   
                    editDialog:server_edit_dialog,
                    searchFunctions: {
                        searchDialog:server_search_dlg
                    },
                    tableModel:server_tbl,
                    columnVisibilityButton:false,
                    columnVisibility:[
                                      {
                                        column:0,
                                        visible:false
                                      }
                                      ]
                };               
                var server_table=new dc2.widgets.TableWidget(server_table_options);
                this._addTabPage("inventory_server",'Servers',server_table);
                server_table.showData();
            }
        },
        _showInventoryXenServer:function(e) {
          if ("inventory_xenserver" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["inventory_xenerver"]]);
          } else {
            this._addTabPage("inventory_xenserver","Xen Server",this.xen_main.getXenHostPage());
          }
        },
        _showInventoryManageVMs:function(e) {
          if ("inventory_xen_vms" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["inventory_xen_vms"]]);
          } else {
            this._addTabPage("inventory_xen_vms","Xen Host Management",this.xen_main.getXenVMSPage());
          }
        },
        _showInventoryNetworks:function(e) {
            if ("inventory_networks" in this._tabPages) {
                this._tabView.setSelection([this._tabPages["inventory_networks"]]);
            } else {
                var networks_tbl=new dc2.models.Networks(dc2.helpers.BrowserCheck.RPCUrl(false));
                var networks_edit_dialog=new dc2.dialogs.EditNetworks();
                var networks_table_options={
                    enableAddEntry:true,
                    enableEditEntry:true,
                    enableDeleteEntry:true,
                    enableReloadEntry:true,
                    editDialog:networks_edit_dialog,
                    addDialog:networks_edit_dialog,
                    tableModel:networks_tbl,
                    columnVisibilityButton:false,
                    columnVisibility:[
                                      {
                                        column:0,
                                        visible:false
                                      }
                                      ]                    
                };
                
                var networks_table=new dc2.widgets.TableWidget(networks_table_options);                                
                this._addTabPage("inventory_networks",'Networks',networks_table);
                networks_table.showData();
            }
        },
        _showDeploymentHosts:function(e) {
          if ("deployment_hosts" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["deployment_hosts"]]);
          } else {
            var hosts_tbl=new dc2.models.Hosts(dc2.helpers.BrowserCheck.RPCUrl(false));
            var hosts_dlg=new dc2.dialogs.EditHosts();
            var hosts_search=new dc2.dialogs.search.Hosts();
            var hosts_options={
                enableAddEntry:false,
                enableEditEntry:true,
                enableDeleteEntry:false,
                enableReloadEntry:true,
                tableModel:hosts_tbl,
                editDialog:hosts_dlg,
                searchFunctions:{
                  searchDialog:hosts_search
                },
                columnVisibilityButton:false,
                columnVisibility:[
                              {
                                column:0,
                                visible:false
                              },
                              {
                                column:1,
                                visible:false
                              }
                              ]
            };
            var hosts_table=new dc2.widgets.TableWidget(hosts_options);
            this._addTabPage("deployment_hosts","Hosts",hosts_table);
            hosts_table.showData();
          }
        },
        _showDeploymentInstallState:function(e) {
          if ("deployment_installstate" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["deployment_installstate"]]);
          } else {
            var installstate_tbl=new dc2.models.InstallState(dc2.helpers.BrowserCheck.RPCUrl(false));
            var installstate_dlg=new dc2.dialogs.EditInstallState();
            var installstate_search=new dc2.dialogs.search.InstallStatus();
            var installstate_options={
                enableAddEntry:false,
                enableEditEntry:true,
                enableDeleteEntry:false,
                enableReloadEntry:true,
                tableModel:installstate_tbl,
                editDialog:installstate_dlg,
                columnVisibilityButton:false,
                searchFunctions:{
                  searchDialog:installstate_search
                },
                columnVisibility:[
                                  {
                                    column:0,
                                    visible:false
                                  },
                                  {
                                    column:1,
                                    visible:false
                                  },
                                  {
                                    column:2,
                                    visible:false
                                  }                                  
                                  ]              
            };
            var installstate_table=new dc2.widgets.TableWidget(installstate_options);
            this._addTabPage("deployment_installstate","Installstate",installstate_table);
            installstate_table.showData();            
          }
        },
        _showConfigurationSettingsDefaultClasses:function(e) {
            if ("configuration_settings_defaultclasses" in this._tabPages) {
                this._tabView.setSelection([this._tabPages["configuration_settings_defaultclasses"]]);
            } else {
                var defclass_tbl=new dc2.models.DefaultClasses(dc2.helpers.BrowserCheck.RPCUrl(false));
                var defclass_edit_dialog=new dc2.dialogs.EditDefaultClasses();
                var defclass_table_options={
                    enableAddEntry:true,
                    enableEditEntry:true,
                    enableDeleteEntry:true,
                    enableReloadEntry:true,
                    tableModel:defclass_tbl,
                    editDialog:defclass_edit_dialog,
                    addDialog:defclass_edit_dialog,
                    columnVisibilityButton:false,
                    columnVisibility:[
                                      {
                                        column:0,
                                        visible:false
                                      }
                                      ]              
                    
                };            
                var defclass_table=new dc2.widgets.TableWidget(defclass_table_options);
                this._addTabPage("configuration_settings_defaultclasses",'Default Classes',defclass_table);
                defclass_table.showData();
            }
        },
        _showConfigurationSettingsEnvironments:function(e) {
            if ("configuration_settings_environments" in this._tabPages) {
                this._tabView.setSelection([this._tabPages["configuration_settings_environments"]]);
            } else {
                var environment_tbl=new dc2.models.Environments(dc2.helpers.BrowserCheck.RPCUrl(false));
                var environment_edit_dialog=new dc2.dialogs.EditEnvironments();
                var environment_tbl_options={
                    enableAddEntry:true,
                    enableEditEntry:true,
                    enableDeleteEntry:true,
                    enableReloadEntry:true,
                    tableModel:environment_tbl,
                    editDialog:environment_edit_dialog,
                    addDialog:environment_edit_dialog,
                    columnVisibilityButton:false,
                    columnVisibility:[
                                      {
                                        column:0,
                                        visible:false
                                      }
                                      ]              
                    
                };               
                //environment_edit_dialog,environment_tbl_options
                var environment_table=new dc2.widgets.TableWidget(environment_tbl_options);
                this._addTabPage("configuration_settings_environments",'Environments',environment_table);
                environment_table.showData();
            }
        },
        _showConfigurationSettingsClassTemplates:function(e) {
          if ("configuration_settings_classtemplates" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["configuration_settings_classtemplates"]]);            
          } else {
            var classtemplates_tbl=new dc2.models.ClassTemplates(dc2.helpers.BrowserCheck.RPCUrl(false));
            var classtemplates_dialog=new dc2.dialogs.EditClassTemplates();
            var classtemplates_options={
                enableAddEntry:true,
                enableEditEntry:true,
                enableDeleteEntry:true,
                enableReloadEntry:true,
                tableModel:classtemplates_tbl,
                addDialog:classtemplates_dialog,
                editDialog:classtemplates_dialog,
                columnVisibility:[
                                  {
                                    column:0,
                                    visible:false
                                  }
                                  ],
                columnVisibilityButton:false                  
                
            };
            var classtemplates_table=new dc2.widgets.TableWidget(classtemplates_options);
            this._addTabPage("configuration_settings_classtemplates","Class Templates",classtemplates_table);
            classtemplates_table.showData();
          }
        },
        _showConfigurationSettingsSystemUsers:function(e) {
          if ("configuration_settings_systemusers" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["configuration_settings_systemusers"]]);            
          } else {
            var systemusers_tbl=new dc2.models.DefaultSystemUsers(dc2.helpers.BrowserCheck.RPCUrl(false));
            var systemusers_dialog=new dc2.dialogs.EditSystemUsers();
            var systemusers_options={
                enableAddEntry:true,
                enableEditEntry:true,
                enableDeleteEntry:true,
                enableReloadEntry:true,
                addDialog:systemusers_dialog,
                editDialog:systemusers_dialog,
                tableModel:systemusers_tbl                
            };
            var systemusers_table=new dc2.widgets.TableWidget(systemusers_options);
            this._addTabPage("configuration_settings_systemusers","Default Systemusers",systemusers_table);
            systemusers_table.showData();
          }
        },
        _showConfigurationSettingsSystemGroups:function(e) {
          if ("configuration_settings_systemgroups" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["configuration_settings_systemgroups"]]);
          } else {
            var systemgroups_tbl=new dc2.models.DefaultSystemGroups(dc2.helpers.BrowserCheck.RPCUrl(false));
            var systemgroups_dlg=new dc2.dialogs.EditSystemGroups();
            var systemgroups_options={
              enableAddEntry:true,
              enableEditEntry:true,
              enableDeleteEntry:true,
              enableReloadEntry:true,
              addDialog:systemgroups_dlg,
              editDialog:systemgroups_dlg,
              tableModel:systemgroups_tbl
            };
            var systemgroups_table=new dc2.widgets.TableWidget(systemgroups_options);
            this._addTabPage("configuration_settings_systemgroups","Default Systemgroups",systemgroups_table);
            systemgroups_table.showData();
          }
        },
        _showConfigurationSettingsBootMethods:function(e) {
          if ("configuration_settings_bootmethods" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["configuration_settings_bootmethods"]]);
          } else {
            var bootmethods_tbl=new dc2.models.DefaultBootmethods(dc2.helpers.BrowserCheck.RPCUrl(false));
            var bootmethods_dialog=new dc2.dialogs.EditDefaultBootmethods();
            var bootmethods_options={
              enableAddEntry:false,
              enableEditEntry:true,
              enableDeleteEntry:false,
              enableReloadEntry:true,
              tableModel:bootmethods_tbl,
              editDialog:bootmethods_dialog,
              extraButtons:[
                { "title":"Update Hardware",
                  "callback":bootmethods_tbl.updateHardware,
                  "context":bootmethods_tbl
                }
              ]
            };
            var bootmethods_table=new dc2.widgets.TableWidget(bootmethods_options);
            this._addTabPage("configuration_settings_bootmethods","Default PXE Bootmethods",bootmethods_table);
            bootmethods_table.showData();
          }
        },
        _showConfigurationPreferences:function(e) {
          if ("configuration_preferences" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["configuration_preferences"]]);
          } else {
            var preferences=new dc2.pages.Preferences();
            this._addTabPage("configuration_preferences", "Preferences", preferences);
          }
        },
        _showConfigurationUsers:function(e) {
          if ("configuration_users" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["configuration_users"]]);            
          } else {
            var configusers_tbl=new dc2.models.Users(dc2.helpers.BrowserCheck.RPCUrl(false));
            var configusers_dlg=new dc2.dialogs.EditUsers();
            var configusers_options={
                enableAddEntry:true,
                enableEditEntry:true,
                enableDeleteEntry:true,
                enableReloadEntry:true,
                tableModel:configusers_tbl,
                addDialog:configusers_dlg,
                editDialog:configusers_dlg
            };
            var configusers_table=new dc2.widgets.TableWidget(configusers_options);
            this._addTabPage("configuration_users","Users",configusers_table);
            configusers_table.showData();
          }
        },
        _showConfigurationGroups:function(e) {
          if ("configuration_groups" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["configuration_groups"]]);            
          } else {
            var configgroups_tbl=new dc2.models.Groups(dc2.helpers.BrowserCheck.RPCUrl(false));
            var configgroups_dlg=new dc2.dialogs.EditGroups();
            var configgroups_options={
                enableAddEntry:true,
                enableEditEntry:true,
                enableDeleteEntry:true,
                enableReloadEntry:true,
                tableModel:configgroups_tbl,
                addDialog:configgroups_dlg,
                editDialog:configgroups_dlg
            };
            var configgroups_table=new dc2.widgets.TableWidget(configgroups_options);
            this._addTabPage("configuration_groups","Groups",configgroups_table);
            configgroups_table.showData();
          }
        },
        //
        // EVENT METHODS
        //
        _closeTabPageEvent:function(e) {
            for (var i in this._tabPages) {
                if (this._tabPages[i]===e.getTarget()) {
                    this._tabPages[i].destroy();
                    delete this._tabPages[i];
                }
            }
        },
        _cs2_mnuHostKeys:function(e) {
          if ("cs2_ssl_keys" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["cs2_ssl_keys"]]);
          } else {
           this._addTabPage("cs2_ssl_keys","CS² SSL Keys",this.cs2_main.getHostKeysPage()); 
          }          
        },
        _cs2_mnuISO3166List:function(e) {
          if ("cs2_ssl_iso3166" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["cs2_ssl_iso3166"]]);
          } else {
            this._addTabPage("cs2_ssl_iso3166","CS² ISO 3166 Country List",this.cs2_main.getISO3166Codes());
          }
        },
        _cs2_mnuCSRs:function(e) {
          if ("cs2_ssl_csrs" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["cs2_ssl_csrs"]]);            
          } else {
            this._addTabPage("cs2_ssl_csrs", "CS² CSRs", this.cs2_main.getCSRPage());
          }
        },
        _cs2_mnuCerts:function(e) {
          if ("cs2_ssl_certs" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["cs2_ssl_certs"]]);            
          } else {
            this._addTabPage("cs2_ssl_certs","CS² Certificates",this.cs2_main.getCertPage());
          }
        },
        _cs2_mnuCrls:function(e) {
          if ("cs2_ssl_crls" in this._tabPages) {
            this._tabView.setSelection([this._tabPages["cs2_ssl_csls"]]);            
          } else {
            this._addTabPage("cs2_ssl_crls","CS² CRLs",this.cs2_main.getCRLPage());
          }
          
        }
        
    }
});
