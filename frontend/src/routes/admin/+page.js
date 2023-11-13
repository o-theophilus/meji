import { redirect, error } from '@sveltejs/kit';

export const load = async ({ parent, fetch, url }) => {

	await fetch(`${import.meta.env.VITE_BACKEND}/admin_init`);
	let a = await parent();
	if (a.locals.user.roles.length == 0) {
		throw error(400, "unauthorized access")
	}
}
