<script context="module">
	import { import.meta.env.VITE_BACKEND } from '$lib/store.js';

	export async function load({ fetch, session, url }) {
		if (session.user.login) {
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}voucher`, {
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
							vouchers: resp.data.vouchers
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
</script>

<script>
	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/comp/button.svelte';

	import Bar from './_bar.svelte';

	import { currency } from '$lib/store.js';

	export let vouchers;
</script>

<svelte:head>
	<title>Voucher | Meji</title>
</svelte:head>

<Card>
	<Title title="Voucher" />
	<Bar />
	<Body>
		{#each vouchers as v}
			<div>
				<Button name="{v.key} - {currency(v.value)} - {v.status}" href="/admin/voucher/{v.key}" />
			</div>
		{:else}
			no voucher
		{/each}
	</Body>
</Card>

<style>
</style>
