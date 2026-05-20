import { error } from '@sveltejs/kit';

export const load = async ({ parent, fetch, params }) => {
	let a = await parent();	

	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/users/${params.username}`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	if (resp.status == 200) {
		return resp
	} else {
		throw error(resp.status, resp.error)
	}
}
