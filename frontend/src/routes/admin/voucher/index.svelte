<script context="module">
	export async function load({ fetch, session, url }) {
		if (session.user.login) {
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}/voucher`, {
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
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';

	import Bar from './_bar.svelte';

	export let vouchers;
</script>

<svelte:head>
	<title>Voucher | Meji</title>
</svelte:head>

<Card>
	<b>Voucher</b>
	<br />
	<br />
	<Bar />
	{#each vouchers as v}
		<div>
			<Button
				name="{v.key} - ₦{v.value.toLocaleString()} - {v.status}"
				href="/admin/voucher/{v.key}"
			/>
		</div>
	{:else}
		no item here
	{/each}
</Card>

<style>
</style>
