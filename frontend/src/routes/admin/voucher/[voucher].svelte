<script context="module">
	export async function load({ fetch, session, params, url }) {
		if (session.user.login) {
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}/voucher/${params.voucher}`, {
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
							voucher: resp.data.voucher,
							logs: resp.data.logs
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

	import { token } from '$lib/cookie.js';

	export let voucher;
	export let logs;

	const submit = async (status) => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}voucher/${voucher.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ status })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				voucher = resp.data.voucher;
				logs = resp.data.logs;
			} else {
				error = resp.message;
			}
		}
	};
</script>

<svelte:head>
	<title>Voucher | Meji</title>
</svelte:head>

<Card>
	<b> Voucher Info </b>
	<br />
	<br />
	Code: {voucher.key}
	<br />
	Value: ₦{voucher.value.toLocaleString()}
	<br />
	Validity: {voucher.validity}
	<br />
	<br />
	Status: {voucher.status}
	{#if voucher.status == 'inactive'}
		<br />
		<Button
			name="Activate"
			on:click={() => {
				submit('active');
			}}
		/>
	{:else if voucher.status == 'active'}
		<br />
		<Button
			name="Deactivate"
			on:click={() => {
				submit('inactive');
			}}
		/>
	{/if}
</Card>
<br />

{#if logs.length > 0}
	<Card>
		<b> Log </b>

		{#each logs as log}
			date: {log.date}
			<br />
			action: {log.action}
			<br />
			result: {log.result}
			<br />
			user key: {log.user_key}
			<br />
			note: {log.note}
			<br />
		{/each}
	</Card>
{/if}

<style>
</style>
