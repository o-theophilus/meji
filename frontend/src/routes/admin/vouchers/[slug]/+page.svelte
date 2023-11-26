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

	let error = {};
	export let data;
	let { voucher } = data;
	$: if ($portal && $portal.type == 'voucher') {
		voucher = $portal.data;
		$portal = '';
	}

	const submit = async (method, url) => {
		error = {};
		$loading = `${method == 'delete' ? 'deleting' : 'deactivating'} . . .`;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/${url}/${voucher.key}`, {
			method: method,
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
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
		{voucher.date.split('T').join(' ')}
	</span>

	<br />

	{voucher.key}

	<br />
	<br />

	<div class="code">
		₦{voucher.value.toLocaleString()}
		<br />

		{voucher.code}{#if voucher.code == '#'}#########{/if}
	</div>

	<br />

	Status: {voucher.status}
	{#if voucher.validity}
		<br />
		Validity: {voucher.validity}
	{/if}

	{#if $user.roles.includes('voucher:status')}
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
						submit('delete', 'voucher');
					}}
				>
					delete
				</Button>
			{:else if voucher.status == 'active'}
				<Button
					on:click={() => {
						submit('put', 'voucher_');
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

{#if $user.roles.includes('log:view')}
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

	.code {
		font-size: large;
		font-weight: 500;
		text-transform: uppercase;

		color: var(--ac1);
	}

	.date {
		font-size: smaller;
		color: var(--ac3);
	}
</style>
