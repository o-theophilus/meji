<script>
	import { user, _tick, module, portal } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';

	import Logout from '../auth/logout.svelte';
	import Button from '$lib/button.svelte';

	import Edit_Photo from './photo_edit.svelte';
	import Delete_Photo from './photo_delete.svelte';
	import Edit_Name from './name.svelte';
	import Edit_Email from './email.svelte';
	import Edit_Phone from './phone.svelte';
	import Edit_Address from './address.svelte';
	import Add_Voucher from './add_voucher.svelte';

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
			<div class="photo_area">
				<img src={$user.photo ? $user.photo : '/image/user.png'} alt={$user.name} />

				<div class="edit">
					{#if edit_mode}
						{#if $user.photo}
							<Delete_Photo {user} />
						{/if}
						<Button
							class="tiny"
							icon="edit"
							icon_size="12"
							on:click={() => {
								$module = {
									module: Edit_Photo,
									user: $user
								};
							}}
						/>
					{/if}
				</div>
			</div>
		</div>

		<div class="details">
			<div class="h space">
				<p>
					<span> Fullname: </span>
					<br />
					{$user.name}
				</p>
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
			<br />

			<div class="h space">
				<p>
					<span> Phone: </span>
					<br />
					{#if $user.phone}
						{$user.phone}
					{:else}
						No Phone
					{/if}
				</p>
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
				{/if}
			</div>

			<br />
			<br />

			<div class="h space">
				<p>
					<span> Address: </span>
					<br />
					{#if $user.address.line && $user.address.local_area && $user.address.state && $user.address.country && $user.address.postal_code}
						{$user.address.line}, {$user.address.local_area} , {$user.address.state} , {$user
							.address.country}.
						<br /><br />
						<span> Postal Code: </span>
						<br />
						{$user.address.postal_code}
					{:else}
						No Address
					{/if}
				</p>

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
				{/if}
			</div>

			<br />
			<br />

			<div class="h space">
				<p>
					<span> Email: </span>
					<br />
					{$user.email}
				</p>
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
				{/if}
			</div>

			<br />
			<br />

			<div class="h">
				<p>
					<span> Account: </span>
					<br />
					Balance: ₦{$user.acc_balance.toLocaleString()}
				</p>
				<Button class="tiny" name="Teansaction History" href="/profile/teansaction_history" />
				<Button
					name="Add Voucher"
					class="tiny"
					icon_size="12"
					on:click={() => {
						$module = {
							module: Add_Voucher,
							user: $user
						};
					}}
				/>
			</div>

			<br />
			<br />

			<div class="h">
				<Button class="tiny" name="Orders" href="/order" />
				<Button class="tiny" name="* Activity" href="/profile/activity" />
			</div>

			<br />
			<br />

			<div class="h">
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
					<Logout />
				{/if}
			</div>

			{#if $user.roles.includes('admin')}
				<Button class="tiny" name="Admin" href="/admin" />
			{/if}
		</div>
	</div>
</Card>

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
	}

	.block {
		gap: var(--sp2);
		display: flex;
		flex-direction: column;

		margin-top: var(--sp2);
	}
	.block > div {
		width: 100%;
	}

	.photo {
		position: relative;
	}
	img {
		width: 100%;
		border-radius: var(--brad1);
	}

	span {
		font-weight: 500;
	}

	.edit {
		position: relative;
		bottom: var(--sp2);
		right: var(--sp2);

		display: flex;
		justify-content: flex-end;
		gap: var(--sp1);
	}
	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
		}

		.photo_area {
			position: sticky;
			top: var(--sp2);
		}
	}
</style>
