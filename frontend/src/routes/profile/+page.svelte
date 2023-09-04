<script>
	import { user, module, portal } from '$lib/store.js';

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

	$: if ($portal) {
		$user = $portal;
		$portal = '';
	}
	let me = true;
	let edit_mode = false;
</script>

<Meta title={$user.name} description={$user.name} />

<Card>
	<div class="title">
		User Details
		{#if me}
			<Button
				name="Edit Mode: {edit_mode ? 'On' : 'Off'}"
				class="tiny"
				icon="edit"
				icon_size="12"
				on:click={() => {
					edit_mode = !edit_mode;
				}}
			/>
		{/if}
	</div>

	<div class="block">
		<div class="photo">
			<Photo {edit_mode} />
		</div>

		<div>
			<div class="horizontal space">
				<b>
					{$user.name}
				</b>
				{#if edit_mode}
					<Button
						class="tiny"
						icon="edit"
						icon_size="12"
						on:click={() => {
							$module = {
								module: Edit_Name,
								user: $user
							};
						}}
					/>
				{/if}
			</div>

			<br />

			<div class="details">
				<span class="bold"> Phone: </span>
				{#if $user.phone}
					{$user.phone}
				{:else}
					No Phone
				{/if}
				{#if edit_mode}
					<Button
						class="tiny"
						icon="edit"
						icon_size="12"
						on:click={() => {
							$module = {
								module: Edit_Phone,
								user: $user
							};
						}}
					/>
				{:else}
					<div />
				{/if}

				<span class="bold"> Email: </span>
				{$user.email}
				{#if edit_mode}
					<Button
						class="tiny"
						icon="edit"
						icon_size="12"
						on:click={() => {
							$module = {
								module: Edit_Email,
								user: $user
							};
						}}
					/>
				{:else}
					<div />
				{/if}

				<span class="bold"> Address: </span>
				{#if $user.address.line && $user.address.local_area && $user.address.state && $user.address.country && $user.address.postal_code}
					{$user.address.line}, {$user.address.local_area}, {$user.address.state}, {$user.address
						.country}.
				{:else}
					No Address
				{/if}

				{#if edit_mode}
					<Button
						class="tiny"
						icon="edit"
						icon_size="12"
						on:click={() => {
							$module = {
								module: Edit_Address,
								user: $user
							};
						}}
					/>
				{:else}
					<div />
				{/if}

				{#if $user.address.line && $user.address.local_area && $user.address.state && $user.address.country && $user.address.postal_code}
					<span class="bold"> Postal Code: </span>
					{$user.address.postal_code}
				{/if}
			</div>

			<br />

			<div class="horizontal">
				<p>
					<span class="bold"> Account: </span>
					<br />
					Balance: ₦{$user.acc_balance.toLocaleString()}
				</p>
				<Button
					name="Add Voucher"
					class="tiny"
					icon_size="12"
					on:click={() => {
						$module = {
							module: Add_Voucher
						};
					}}
				/>
			</div>

			<br />

			<div class="horizontal">
				<Button class="tiny" name="Orders" href="/orders" />
				<Button class="tiny" name="Logs" href="/profile/logs" />
			</div>

			<br />

			<div class="horizontal">
				{#if me}
					{#if edit_mode}
						<Button
							class="tiny"
							name="setting"
							icon="setting"
							icon_size="12"
							href="/profile/setting"
						/>
					{/if}
					{#if $user.roles.includes('admin')}
						<Button class="tiny" name="Admin" href="/admin" />
					{/if}
					<Logout />
				{/if}
			</div>
		</div>
	</div>
</Card>

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.block {
		gap: var(--sp3);
		display: flex;
		flex-direction: column;

		margin-top: var(--sp2);
	}
	.block > div {
		width: 100%;
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

	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
		}
	}
</style>
