# 🌳 Git Workflow - Caja Negra

## Estructura de Ramas

```
main (producción → GitHub Pages)
 ↓
develop (integración)
 ├── feature/audios (audios MP3 y reproducción)
 ├── feature/video (videos e integración)
 ├── feature/gameplay (mecánica del juego)
 └── feature/ui (interfaz y diseño)
```

## Flujo de Trabajo

### 1️⃣ Trabajar en una Feature
```bash
# Cambiar a develop
git checkout develop
git pull origin develop

# Crear/usar feature branch
git checkout feature/audios
git pull origin feature/audios

# Hacer cambios
# ...

# Commit
git add .
git commit -m "Descripción clara del cambio"
git push origin feature/audios
```

### 2️⃣ Mergear a Develop (cuando feature está lista)
```bash
git checkout develop
git pull origin develop
git merge feature/audios
git push origin develop
```

### 3️⃣ Mergear a Main (cuando develop está listo para producción)
```bash
git checkout main
git pull origin main
git merge develop
git push origin main
# GitHub Pages se actualiza automáticamente
```

## Branches Disponibles

| Rama | Propósito |
|------|-----------|
| `main` | Producción (GitHub Pages) - **NO editar directamente** |
| `develop` | Rama de integración - punto de encuentro de features |
| `feature/audios` | Sistema de audios MP3 |
| `feature/video` | Videos e integración |
| `feature/gameplay` | Mecánica de juego |
| `feature/ui` | Interfaz y estilos |

## Reglas

✅ **SIEMPRE**
- Trabajar en feature branches
- Hacer commit antes de cambiar de rama
- Hacer pull antes de trabajar

❌ **NUNCA**
- Editar `main` directamente
- Hacer force push (`git push --force`)
- Borrar ramas sin confirmación

## Estado Actual

- `main`: Versión en GitHub Pages (producción)
- `develop`: Rama de desarrollo (lista para features)
- Todas las features: Creadas y listas para usar

---
**Creado:** 2026-11-03  
**Última actualización:** 2026-11-03
