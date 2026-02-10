import { error } from '@sveltejs/kit';

export const load = async ({ parent, fetch, params }) => {
	let a = await parent();
	if (!a.locals.user.access.includes("coupon:view")) {
		throw error(400, "Unauthorized access")
	}
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/coupon/${params.slug}`, {
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
