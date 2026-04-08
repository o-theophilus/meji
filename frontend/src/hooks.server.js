import { error } from '@sveltejs/kit';

export async function handle({ event, resolve }) {
    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/init`, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            Authorization: event.cookies.get("token")
        }
    });
    resp = await resp.json();

    if (resp.status == 200) {
        event.locals = resp;
        return await resolve(event);
    }

    throw error(404, `Error status: ${resp.status}`)
}