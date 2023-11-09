import { redirect, error } from '@sveltejs/kit';

export const load = async ({ parent, fetch, url }) => {

	await fetch(`${import.meta.env.VITE_BACKEND}/admin_init`);
	let a = await parent();

	// if(!a.locals.user.login){
	// 	throw redirect(307, `/?module=login&return_url=${url.pathname}`);
	// }
	// else if(!a.locals.user.roles.includes('admin')){
	// 	throw error(400, "unauthorized access")
	// }
	if (a.locals.user.roles.length == 0) {
		throw error(400, "unauthorized access")
	}
}
