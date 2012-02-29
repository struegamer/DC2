qx.Class.define("menucreator.MenuCreator",
    {
      extend: qx.core.Object,
      construct:function() {
        this.base(arguments);
      },
      members: {
            menuBar:null,
            getMenuBar:function(menuHash) {            
                this.menuBar=this.createMenu(menuHash);
                return this.menuBar;
            },
            createMenu:function(menuHash) {
                var menu=new qx.ui.menubar.MenuBar();
                for (var i=0;i<menuHash.items.length;++i) {
                    if (menuHash.items[i].type=="menu") {
                        var submenu=this.createSubMenu(menuHash.items[i].items);
                        if (submenu != null) {
                            var menuButton=new qx.ui.menubar.Button(menuHash.items[i].name,null,submenu);
                        } else {
                            var menuButton=new qx.ui.menubar.Button(menuHash.items[i].name,null);
                        }
                        menu.add(menuButton);
                    }
                }
                return(menu);
            },
            createSubMenu:function(menuItems) {
                console.log("createSubMenu");
                if (menuItems != null) {
                    var submenu=new qx.ui.menu.Menu();
                    for (var i=0;i<menuItems.length;++i) {
                        if (menuItems[i].type=="button") {                           
                            var menubutton=new qx.ui.menu.Button(menuItems[i].name,menuItems[i].icon);
                            if (menuItems[i].callback != null) {
                                if (menuItems[i].context!=null) {
                                    menubutton.addListener("execute",menuItems[i].callback,menuItems[i].context);
                                } else {
                                    menubutton.addListener("execute",menuItems[i].callback);
                                }
                            }
                            submenu.add(menubutton);
                        }                        
                        if (menuItems[i].type=="separator") {
                            var menusep=new qx.ui.menu.Separator();
                            submenu.add(menusep);
                        }
                        if (menuItems[i].type=="submenu") {
                            var menusubmenu=this.createSubMenu(menuItems[i].items);
                            var menubutton=new qx.ui.menu.Button(menuItems[i].name,menuItems[i].icon,null,menusubmenu);
                            submenu.add(menubutton);                            
                        }
                        if (menuItems[i].type=="checkbox") {
                            var menucheckbox=new qx.ui.menu.CheckBox(menuItems[i].name);
                        }
                   }
                   return(submenu);
               } else {
                return(null);
               }        
            }
        }
    }
);
