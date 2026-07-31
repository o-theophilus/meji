import { error } from '@sveltejs/kit';

export const load = async ({ fetch, url, parent, depends }) => {
	depends(true)

	let a = await parent();
	if (
		!a.locals.user.access.includes("admin.tag.featured")
		|| !a.locals.user.access.includes("admin.tag.rename")
		|| !a.locals.user.access.includes("admin.tag.delete")
	) {
		throw error(403, "Unauthorized access")
	}

	return
}
