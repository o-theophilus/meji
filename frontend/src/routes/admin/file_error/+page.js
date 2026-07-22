import { error } from '@sveltejs/kit';

export const load = async ({ parent, fetch }) => {
	let a = await parent();
	if (!a.locals.user.access.includes("admin.manage_files")) {
		throw error(404, "Unauthorized access")
	}

	let result = await fetch(`${import.meta.env.VITE_BACKEND}/file_error`, {
		method: 'get',
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
