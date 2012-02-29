/* ************************************************************************
   Copyright:
   License:
   Authors:
************************************************************************ */

/* ************************************************************************
#asset(menucreator/*)
************************************************************************ */
/**
 * This is the main application class of your custom application "menucreator"
 */
qx.Class.define("menucreator.Application",
{
  extend : qx.application.Standalone,
  /*
  *****************************************************************************
     MEMBERS
  *****************************************************************************
  */
  members :
  {
    /**
     * This method contains the initial application code and gets called 
     * during startup of the application
     * 
     * @lint ignoreDeprecated(alert)
     */
    main : function()
    {
      // Call super class
      this.base(arguments);

      // Enable logging in debug variant
  
        // support native logging capabilities, e.g. Firebug for Firefox
        qx.log.appender.Native;
        // support additional cross-browser console. Press F7 to toggle visibility
        qx.log.appender.Console;
   

      var menuHash={
        items: [
            { 
                name: "File",
                type: "menu",
                items: [
                    { 
                        name: "New",
                        type: "button",
                        callback:this.newButton
                    },
                    {
                        name:"",
                        type:"separator"
                    },
                    {
                        name:"Open",
                        type:"button",
                        callback:null
                    }                       
                ]
            },
            {
                name: "Edit",
                type:"menu",
                items:null
            }
        ]
      };
      var mainMenuObj=new menucreator.MenuCreator();
      var mainMenu=mainMenuObj.getMenuBar(menuHash);
      console.log("here");

      // Document is the application root
      var doc = this.getRoot();
      var container=new qx.ui.container.Composite(new qx.ui.layout.Dock()).set({decorator:'main',allowGrowY:true});
      container.add(mainMenu,{edge:'north'});
      doc.add(container);
      
    },
    createMenu:function(menuHash) {
        console.log("createMenu");
        var menu=new qx.ui.menubar.MenuBar();
        for (var i=0;i<menuHash.items.length;++i) {
            console.log("counter: "+i);
            console.log("menuHash: "+menuHash.items[i]);
            if (menuHash.items[i].type=="menu") {
                console.log("menuHash.items[i].name => "+menuHash.items[i].name);
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
                console.log("menuItems.name "+menuItems[i].name);
                if (menuItems[i].type=="button") {
                    var menubutton=new qx.ui.menu.Button(menuItems[i].name);
                    if (menuItems[i].callback != null) {
                        menubutton.addListener("execute",menuItems[i].callback,this);
                    }
                    submenu.add(menubutton);
                }
                if (menuItems[i].type=="separator") {
                    var menusep=new qx.ui.menu.Separator();
                    submenu.add(menusep);
                }
           }
           return(submenu);
       } else {
        return(null);
       }
    },
    newButton:function(e) {
        console.log("works for new");
    }
  }
});
