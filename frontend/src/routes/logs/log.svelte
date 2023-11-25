<script>
	import { user, set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';

	export let log;
	export let page_name;

	let href = '';
	if (log.entity.type == 'item') {
		href = `/${log.entity.key}`;
	} else if (log.entity.type == 'order') {
		href = `/orders/${log.entity.key}`;
	} else if (log.entity.type == 'voucher') {
		href = `/admin/vouchers/${log.entity.key}`;
	} else if (log.entity.type == 'advert') {
		href = `/${log.entity.key.split('_')[0]}?edit=true&advert=true`;
	}
</script>

<section>
	<div
		class="status"
		class:good={log.status == 200}
		class:caution={![200, 400].includes(log.status)}
		class:error={log.status == 400}
	/>
	{log.date}
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
				set_state(page_name, 'search', `${log.user.key}:all:all:all`);
			}}
		>
			^
		</Button>
	{/if}

	{log.action}

	{#if log.entity.type != 'auth'}
		{log.entity.type}

		<Button class="link" {href}>
			{#if log.entity.name}
				{log.entity.name}
			{:else}
				{log.entity.key}
			{/if}
		</Button>
	{/if}

	{#if log.misc}
		{#each Object.entries(log.misc) as [key, value]}
			<br />
			{key}: {value}
		{/each}
	{/if}
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
</style>
