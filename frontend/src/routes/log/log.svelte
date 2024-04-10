<script>
	import { user } from '$lib/store.js';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();
	export let log;

	let href = '';
	if (log.entity_type == 'item') {
		href = `/${log.entity_key}`;
	} else if (log.entity_type == 'order') {
		href = `/orders/${log.entity_key}`;
	} else if (log.entity_type == 'voucher') {
		href = `/admin/vouchers/${log.entity_key}`;
	} else if (log.entity_type == 'advert') {
		href = `/admin/adverts/${log.entity_key}`;
	} else if (log.entity_type == 'page') {
		href = log.entity_key;
	} else if (['user', 'admin'].includes(log.entity_type) && log.entity_key) {
		href = `/profile?search=${log.entity_key}`;
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

	<a href="/profile?search={log.user_key}">
		{log.user_name}
	</a>

	{#if log.user_key && $user.permissions.includes('log:view')}
		<button
			on:click={() => {
				emit('search', { u: log.user_key });
			}}
		>
			&#9679;
		</button>
	{/if}

	{#if log.entity_type == 'page'} viewed {:else} {log.action} {/if}

	{#if log.entity_type == 'user' && log.action == 'viewed' && !log.entity_key}
		profile
	{/if}

	{#if href}
		{log.entity_type}

		<a {href}>
			{log.entity_name}
		</a>

		<button
			on:click={() => {
				emit('search', { e: log.entity_key });
			}}
		>
			&#9679;
		</button>
	{/if}

	{#if log.misc}
		<br />
		{#each Object.entries(log.misc) as [key, value]}
			{key}: {value}
			<br />
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
		background-color: var(--cl6);
	}
	.error {
		background-color: var(--cl4);
	}

	/* .bold {
		font-weight: 700;
	} */

	.date {
		font-size: smaller;
		color: var(--ac3);
	}

	a {
		color: var(--cl1);
		text-decoration: none;
		font-weight: 700;
	}
	button {
		color: var(--cl1);
		border: none;
		background-color: transparent;
		cursor: pointer;
	}

	button:hover,
	a:hover {
		color: var(--cl1_b);
	}
</style>
