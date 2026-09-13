# Adapter Contract

Every external integration added to executable code should conform conceptually to this contract.

```ts
interface CreativeIntegrationAdapter<TInstance = unknown> {
  id: string
  upstream: string
  capability: string[]
  performanceTier: 'low' | 'medium' | 'high'
  ssr: 'safe' | 'client-only' | 'adapter-required'
  reducedMotion: 'native' | 'local-fallback' | 'not-applicable'
  init(ctx: CreativeRuntimeContext): TInstance
  destroy(instance: TInstance): void
  getEscapeHatch(instance: TInstance): TInstance
}
```

Adapters must not hide upstream APIs so deeply that creative developers cannot tune advanced behavior.
