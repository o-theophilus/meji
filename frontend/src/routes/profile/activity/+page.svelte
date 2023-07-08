<!-- <script context="module">
	export async function load({ fetch, session, url }) {
		if (session.user.login) {
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}/activity`, {
				method: 'get',
				headers: {
					'Content-Type': 'application/json',
					Authorization: session.token
				}
			});

			if (_resp.ok) {
				let resp = await _resp.json();

				if (resp.status == 200) {
					return {
						props: {
							activity: resp.data.activity
						}
					};
				} else {
					return {
						status: 404,
						error: resp.message
					};
				}
			}
		}
		return {
			status: 302,
			redirect: `/?module=login&return_url=${url.pathname}`
		};
	}
</script> -->

<script>
	import { user } from '$lib/store.js';

	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';

	export let activity = [];
</script>

<svelte:head>
	<title>Activity | Meji</title>
</svelte:head>

<Card>
	<Title title="Activity" />
	<Body>
		{#each activity as act}
			{act.key} - {act.value}
			<br />
		{/each}
	</Body>
</Card>
