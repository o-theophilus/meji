<script>
	import { portal, loading, module, toast, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Center from '$lib/center.svelte';
	import Logs from './logs.svelte';
	import Activate from './_activate.svelte';
	import Back from '$lib/button.back.svelte';

	export let data;
	let { voucher } = data;
	let error = {};

	$: if ($portal && $portal.type == 'voucher') {
		voucher = $portal.data;
		$portal = '';
	}

	const submit = async (status) => {
		error = {};
		$loading = `${status == 'delete' ? 'deleting' : 'deactivating'} . . .`;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/voucher/status/${voucher.key}`, {
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

<Meta title="Manage Voucher" />

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			Voucher
		</div>
	</div>
</Center>

<Card>
	<span class="date">
		{voucher.date}
	</span>

	<br />

	{voucher.key}

	<br />
	<br />

	<div class="pin">
		₦{voucher.value.toLocaleString()}
		<br />

		{voucher.pin}{#if voucher.pin == '#'}#########{/if}
	</div>

	<br />

	Status: {voucher.status}
	{#if voucher.validity}
		<br />
		Validity: {voucher.validity}
	{/if}

	{#if $user.permissions.includes('voucher:status')}
		{#if ['active', 'inactive'].includes(voucher.status)}
			<br />
			<br />
		{/if}

		<div class="horizontal">
			{#if voucher.status == 'inactive'}
				<Button
					on:click={() => {
						$module = {
							module: Activate,
							voucher
						};
					}}
				>
					Activate
				</Button>
				<Button
					on:click={() => {
						submit('delete');
					}}
				>
					delete
				</Button>
			{:else if voucher.status == 'active'}
				<Button
					on:click={() => {
						submit('deactivate');
					}}
				>
					deactivate
				</Button>
			{/if}
		</div>
	{/if}

	{#if error.error}
		<br />
		<div class="error">{error.error}</div>
	{/if}
</Card>

{#if $user.permissions.includes('log:view')}
	{#key `${voucher.key}_${voucher.status}`}
		<Logs voucher_key={voucher.key} />
	{/key}
{/if}

<style>
	.horizontal {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.pin {
		font-size: large;
		font-weight: 700;
		text-transform: uppercase;

		color: var(--ac1);
	}

	.date {
		font-size: smaller;
		color: var(--ac3);
	}
</style>
