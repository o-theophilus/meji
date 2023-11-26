<script>
	import { user } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();
	export let log;

	let href = '';
	if (log.entity.type == 'item') {
		href = `/${log.entity.key}`;
	} else if (log.entity.type == 'order') {
		href = `/orders/${log.entity.key}`;
	} else if (log.entity.type == 'voucher') {
		href = `/admin/vouchers/${log.entity.key}`;
	} else if (log.entity.type == 'advert') {
		href = `/admin/adverts/${log.entity.key}`;
	}
</script>

<section>
	<div
		class="status"
		class:good={log.status == 200}
		class:caution={![200, 400].includes(log.status)}
		class:error={log.status == 400}
	/>
	<span class="date">
		{log.date.split('T').join(' ')}
	</span>
	<br />

	{#if log.user.name == 'deleted_user'}
		<span class="bold"> Deleted User </span>
	{:else}
		<Button class="link" href="/profile?search={log.user.key}">
			{log.user.name}
		</Button>
	{/if}

	{#if $user.roles.includes('log:view')}
		<Button
			class="link"
			on:click={() => {
				emit('search', { user: log.user.key });
			}}
		>
			&#9679;
		</Button>
	{/if}

	{log.action}

	{#if log.entity.type}
		{log.entity.type}
	{/if}

	{#if log.entity.key}
		<Button class="link" {href}>
			{log.entity.name}
		</Button>

		<Button
			class="link"
			on:click={() => {
				emit('search', { entity: log.entity.key });
			}}
		>
			&#9679;
		</Button>
	{/if}

	{#each Object.entries(log.misc) as [key, value]}
		<br />
		<span class="break">
			{key}: {value}
		</span>
	{/each}
</section>

<style>
	section {
		padding: var(--sp2) 0;
		border-bottom: 2px solid var(--ac5);
	}

	.status {
		display: inline-block;
		--size: 10px;
		width: var(--size);
		height: var(--size);

		border-radius: 50%;

		background-color: var(--cl5);
		color: var(--ac6_);
	}
	.good {
		background-color: var(--cl5);
	}
	.caution {
		background-color: var(--cl3);
	}
	.error {
		background-color: var(--cl4);
	}

	.bold {
		font-weight: 500;
	}

	.date {
		font-size: smaller;
		color: var(--ac3);
	}

	.break {
		word-wrap: break-word;
		word-break: break-all;
	}
</style>
