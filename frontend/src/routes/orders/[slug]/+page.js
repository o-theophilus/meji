import { error } from '@sveltejs/kit';

export const load = async ({ fetch, parent, params }) => {
	let a = await parent();
	let response = await fetch(`${import.meta.env.VITE_BACKEND}/orders/${params.slug}`, {
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	let result = await response.json();

	if (response.status == 200) {
		return result
	} else {
		throw error(result.status, result.error)
	}
}