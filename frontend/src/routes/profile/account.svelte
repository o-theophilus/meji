<script>
	import { user as me, module } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Add_Voucher from './_voucher.svelte';

	export let user;
</script>

<div class="row">
	<span>
		<span class="bold"> Account: </span>
		<br />
		Balance:

		{#if user.account_balance != '#'}
			₦{user.account_balance.toLocaleString()}
		{:else}
			{user.account_balance}##
		{/if}
		{#if user.key == $me.key}
			<br />
			<Link href="/profile/transaction">Transactions</Link>
		{/if}
	</span>

	{#if user.key == $me.key}
		<Button
			on:click={() => {
				$module = {
					module: Add_Voucher
				};
			}}
		>
			Add Voucher
		</Button>
	{/if}
</div>

<style>
	.bold {
		font-weight: 700;
	}

	.row {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}
</style>
