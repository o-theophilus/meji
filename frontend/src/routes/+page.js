export const load = async ({ fetch }) => {
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/home`)
	resp = await resp.json();

	if (resp.status == 200) {
		return resp
	}
}
