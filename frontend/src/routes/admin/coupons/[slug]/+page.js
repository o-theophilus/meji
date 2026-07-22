import { error } from '@sveltejs/kit';

export const load = async ({ parent, fetch, params }) => {
	let a = await parent();
	if (!a.locals.user.access.includes("coupon.view")) {
		throw error(400, "Unauthorized access")
	}
	let result = await fetch(`${import.meta.env.VITE_BACKEND}/coupons/${params.slug}`, {
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	result = await result.json();
	if (result.status == 200) {
		return result
	} else {
		throw error(result.status, result.error)
	}
}
