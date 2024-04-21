<script>
	import { portal, module, user } from '$lib/store.js';
	import Datetime from '$lib/datetime.svelte';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Button from '$lib/button.svelte';
	import Center from '$lib/center.svelte';
	import Logs from './logs.svelte';
	import Activate from './_activate.svelte';
	import Status from './_status.svelte';
	import Back from '$lib/button.back.svelte';

	export let data;
	let { voucher } = data;

	let { logs } = data;
	let error = {};

	$: if ($portal) {
		if ($portal.voucher) {
			voucher = $portal.voucher;
		}
		if ($portal.logs) {
			logs = $portal.logs;
		}
		$portal = '';
	}

	$: if (voucher.validity) {
		voucher.validity = new Date(voucher.validity);
		voucher.validity.setDate(voucher.validity.getDate() - 1);
	}
</script>

<Meta title="Manage Voucher" />
<Log action={'viewed'} entity_key={voucher.key} entity_type={'voucher'} />

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
		<Datetime datetime={voucher.date} type="date" />
		<Datetime datetime={voucher.date} type="time" />
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

	Status: <span class="status"> {voucher.status}</span>
	{#if voucher.validity}
		<br />
		Validity:
		<Datetime datetime={voucher.validity} type="date" />
	{/if}

	{#if $user.permissions.includes('voucher:status')}
		{#if ['created', 'activated', 'deactivated'].includes(voucher.status)}
			<br />
			<br />
		{/if}

		<div class="horizontal">
			{#if ['created', 'deactivated'].includes(voucher.status)}
				<Button
					on:click={() => {
						$module = {
							module: Activate,
							key: voucher.key
						};
					}}
				>
					Activate
				</Button>

				<Button
					on:click={() => {
						$module = {
							module: Status,
							key: voucher.key,
							status: 'deleted'
						};
					}}
				>
					delete
				</Button>
			{:else if voucher.status == 'activated'}
				<Button
					on:click={() => {
						$module = {
							module: Status,
							key: voucher.key,
							status: 'deactivated'
						};
					}}
				>
					Deactivate
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
	<Logs {logs} voucher_key={voucher['key']} />
{/if}

<style>
	.horizontal {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.date {
		font-size: smaller;
		color: var(--ac3);
	}

	.pin {
		font-size: large;
		font-weight: 700;
		text-transform: uppercase;

		color: var(--ac1);
	}

	.status {
		text-transform: capitalize;
	}
</style>
