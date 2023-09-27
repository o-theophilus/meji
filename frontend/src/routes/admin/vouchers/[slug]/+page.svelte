<script>
	import { portal, loading, module, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Log from '../../logs/log.svelte';
	import Activate from './_activate.svelte';

	let error = {};
	export let data;
	let { voucher } = data;
	$: if ($portal && $portal.type == 'voucher') {
		voucher = $portal.data;
		$portal = '';
	}

	const submit = async (status) => {
		error = {};
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/voucher/${voucher.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ status })
		});

		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			voucher = resp.voucher;
			$module = '';
			$toast = {
				status: 200,
				message: 'Voucher status changed'
			};
		} else {
			error = resp;
		}
	};
</script>

<Meta title="Voucher" description="Voucher" />

<Card>
	<b> Voucher{voucher.length > 1 ? 's' : ''} </b>
	<br />
	<br />
	{voucher.date}
	<br />
	<a href="/admin/vouchers/{voucher.key}">
		{voucher.key}
	</a>
	<br />
	<div class="code">
		₦{voucher.value.toLocaleString()}
		<br />
		{voucher.code}
	</div>

	Status: {voucher.status}
	{#if voucher.validity}
		<br />
		Validity: {voucher.validity}
	{/if}
	<br />
	<br />
	<div class="horizontal">
		{#if voucher.status == 'inactive'}
			<Button
				class="small"
				on:click={() => {
					$module = {
						module: Activate,
						voucher
					};
				}}
			>
				Activate
			</Button>
		{:else}
			<Button
				class="small"
				on:click={() => {
					submit('inactive');
				}}
			>
				deactivate
			</Button>
		{/if}
		<Button
			class="small"
			on:click={() => {
				submit('delete');
			}}
		>
			delete
		</Button>
	</div>
	{#if error.error}
		<br />
		<div class="error">{error.error}</div>
	{/if}
	<br />
	<b> Log{voucher.logs.length > 1 ? 's' : ''} </b>
	<br />
	<br />

	{#each voucher.logs as log}
		<Log {log} />
	{:else}
		no item here
	{/each}
</Card>

<style>
	.horizontal {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.code {
		font-size: large;
		font-weight: 500;
		text-transform: uppercase;
	}
</style>
