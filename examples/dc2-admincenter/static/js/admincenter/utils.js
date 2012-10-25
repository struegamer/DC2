/**
 * 
 */
function unbind_buttons(btn_class_selector,event_name,func) {
	btn_class_selector.each(function () {
		$(this).off(event_name,func);
	});
}

function bind_buttons(btn_class_selector,event_name,selector,func,context) {
	btn_class_selector.on(event_name,selector,func.bind(context));
}