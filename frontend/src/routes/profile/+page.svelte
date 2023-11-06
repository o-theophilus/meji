<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user as me, module, portal, set_state } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';

	import Button from '$lib/button.svelte';
	import Logout from '../auth/logout.svelte';

	import Photo from './photo.svelte';
	import Edit_Name from './_name.svelte';
	import Edit_Email from './_email.svelte';
	import Edit_Phone from './_phone.svelte';
	import Edit_Address from './_address.svelte';
	import Add_Voucher from './_voucher.svelte';
	import SVG from '$lib/svg.svelte';
	import Search from '$lib/search.svelte';
	import Center from '$lib/center.svelte';
	import Role from './role.svelte';

	export let data;
	$: user = data.user;
	$: console.log(data.user);

	let edit_mode = false;
	let page_name = 'profile';

	$: if ($portal && $portal.type == 'user') {
		user = $portal.data;
		$portal = '';
	}

	let search = '';
	let _search = '';
	const submit = () => {
		if (_search != search) {
			_search = `${search}`;
			set_state(page_name, 'search', search);
		}
	};
	onMount(async () => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
			_search = params.get('search');
		}
	});
</script>

<Meta title={user?.name} description={user?.name} />

<Center>
	<br />
	<div class="ctitle">
		User Details
		{#if user && user.key == $me.key}
			<Button
				class="small"
				on:click={() => {
					edit_mode = !edit_mode;
				}}
			>
				<SVG type="edit" size="12" />
				Edit: {edit_mode ? 'On' : 'Off'}
			</Button>
		{/if}
	</div>
</Center>

<Card>
	{#if $me.roles.includes('admin')}
		<div class="line">
			<Search
				placeholder="Search for User by  Email or Key"
				bind:search
				on:ok={() => {
					submit();
				}}
				on:clear={() => {
					search = '';
					submit();
				}}
			/>
			<Button class="primary" on:click={submit} disabled={search == _search}>Search</Button>
		</div>

		<br />
	{/if}

	{#if data.error}
		<span class="error">
			{data.error}
		</span>
	{:else}
		<div class="block">
			<div class="photo">
				<Photo {edit_mode} />
			</div>

			<div>
				<div class="horizontal space">
					<span class="name">
						{user.name}
					</span>
					{#if edit_mode}
						<Button
							class="small round"
							tooltip="Edit Name"
							on:click={() => {
								$module = {
									module: Edit_Name,
									user: user
								};
							}}
						>
							<SVG type="edit" size="12" />
						</Button>
					{/if}
				</div>

				<br />

				<div class="details">
					<span class="bold"> Phone: </span>
					{#if user.phone}
						{user.phone}
					{:else}
						No Phone
					{/if}
					{#if edit_mode}
						<Button
							class="small round"
							tooltip="Edit Phone Number"
							on:click={() => {
								$module = {
									module: Edit_Phone,
									user: user
								};
							}}
						>
							<SVG type="edit" size="12" />
						</Button>
					{:else}
						<div />
					{/if}

					<span class="bold"> Email: </span>
					{user.email}
					{#if edit_mode}
						<Button
							class="small round"
							tooltip="Edit Email"
							on:click={() => {
								$module = {
									module: Edit_Email,
									user: user
								};
							}}
						>
							<SVG type="edit" size="12" />
						</Button>
					{:else}
						<div />
					{/if}

					<span class="bold"> Address: </span>
					{#if user.address.line && user.address.local_area && user.address.state && user.address.country && user.address.postal_code}
						{user.address.line}, {user.address.local_area}, {user.address.state}, {user.address
							.country}.
					{:else}
						No Address
					{/if}

					{#if edit_mode}
						<Button
							class="small round"
							tooltip="Edit Address"
							on:click={() => {
								$module = {
									module: Edit_Address,
									user: user
								};
							}}
						>
							<SVG type="edit" size="12" />
						</Button>
					{:else}
						<div />
					{/if}

					{#if user.address.line && user.address.local_area && user.address.state && user.address.country && user.address.postal_code}
						<span class="bold"> Postal Code: </span>
						{user.address.postal_code}
					{/if}
				</div>

				<br />

				<div class="horizontal">
					<p>
						<span class="bold"> Account: </span>
						<br />
						Balance: ₦{user.acc_balance.toLocaleString()}
					</p>
					{#if user.key == $me.key}
						<Button
							class="small"
							on:click={() => {
								$module = {
									module: Add_Voucher
								};
							}}
						>
							Add Voucher
						</Button>
						<Button class="small" href="/profile/transaction">Transaction</Button>
					{/if}
				</div>

				<br />

				{#if user.key == $me.key}
					<div class="horizontal">
						<Button class="small" href="/orders">Orders</Button>
						{#if user.roles.includes('admin')}
							<Button class="small" href="/admin">Admin</Button>
						{/if}
						{#if edit_mode}
							<Button class="small" href="/profile/setting">
								<SVG type="setting" size="12" />
								Setting
							</Button>
						{/if}
					</div>

					<br />

					<div class="horizontal">
						<Logout />
					</div>
				{/if}
			</div>
		</div>
	{/if}
</Card>

{#if user.key != me.key && user.status == 'confirm' && me.roles.includes('admin')}
	<Role {user} />
{/if}

<style>
	.block {
		gap: var(--sp3);
		display: flex;
		flex-direction: column;
	}
	.block > div {
		width: 100%;
	}

	.name {
		font-weight: 600;
		color: var(--ac1);
	}
	.bold {
		font-weight: 500;
	}

	.horizontal {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}
	.space {
		justify-content: space-between;
	}

	.details {
		display: grid;
		gap: 0 var(--sp2);
		grid-template-columns: max-content auto min-content;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}

	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
		}
	}
</style>
